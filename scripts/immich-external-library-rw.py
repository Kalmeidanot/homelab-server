#!/usr/bin/env python3
"""Apply the explicitly approved RO->RW archive bind; never delete/write media.
Run once with sudo and --apply. Config secrets stay in memory and are not logged.
Evidence/backups are outside Git in the active archive control area.
"""
import argparse, copy, datetime, fcntl, hashlib, json, os, pathlib, re, stat, subprocess, sys, time, urllib.request
ROOT=pathlib.Path('/home/kaian/nas-admin')
COMPOSE=ROOT/'compose/immich/docker-compose.yml'
CONTROL=pathlib.Path('/home/kaian/media-archive-control/_merge-control/server-changes/immich-external-rw')
SOURCE='/srv/storage/archive/merged/Bilder og Video'
TARGET='/mnt/archive/bilder-og-video'
TEST_DIR=pathlib.Path(SOURCE)/'Disposeable'
TEST_FILE=TEST_DIR/'Xenomorph.jpg'
OLD="      - '/srv/storage/archive/merged/Bilder og Video:/mnt/archive/bilder-og-video:ro'"
NEW="      - '/srv/storage/archive/merged/Bilder og Video:/mnt/archive/bilder-og-video:rw'"
NAMES=['immich_server','immich_machine_learning','immich_postgres','immich_redis']
EXPECTED_SHA='418af8fcc6c74d352cdfc8c16131c04bd0bcc1a4f7a6d41b0ee070d6acf53fc8'
report={'success':False,'applied':False,'payload_write_test':False,'payload_deleted':False,'hidden_accessed':False,'host_permissions_changed':False}

def run(args, *, input=None, check=True):
 p=subprocess.run(args,input=input,text=True,capture_output=True,cwd=COMPOSE.parent,timeout=180)
 if check and p.returncode:raise RuntimeError('Command failed (output withheld to protect secrets): '+ ' '.join(args[:5]))
 return p

def dc(*args,input=None):return run(['docker','compose',*args],input=input)
def config(text):return json.loads(dc('-f','-','--project-directory',str(COMPOSE.parent),'config','--format','json',input=text).stdout)
def inspect():return {x['Name'].lstrip('/'):x for x in json.loads(run(['docker','inspect',*NAMES]).stdout)}
def safe_summary(xs):
 return {n:{'id':x['Id'],'image_id':x['Image'],'image':x['Config']['Image'],'status':x['State']['Status'],'health':x['State'].get('Health',{}).get('Status'),'restart_count':x['RestartCount'],'restart_policy':x['HostConfig']['RestartPolicy'],'mounts':x['Mounts'],'compose_project':x['Config']['Labels'].get('com.docker.compose.project'),'compose_service':x['Config']['Labels'].get('com.docker.compose.service')} for n,x in xs.items()}
def healthy(xs):return all(x['State']['Running'] and not x['State']['Restarting'] and x['State'].get('Health',{}).get('Status','healthy')=='healthy' for x in xs.values())
def http():
 with urllib.request.urlopen('http://127.0.0.1:2283/',timeout=5) as r:code=r.status
 with urllib.request.urlopen('http://127.0.0.1:2283/api/server/version',timeout=5) as r:version=json.load(r)
 assert code==200;return {'web_status':code,'version':version}
def proof(p):
 s=os.lstat(p);assert not stat.S_ISLNK(s.st_mode)
 out={'path':str(p),'dev':s.st_dev,'inode':s.st_ino,'size':s.st_size,'mtime_ns':s.st_mtime_ns,'ctime_ns':s.st_ctime_ns,'mode':stat.S_IMODE(s.st_mode),'uid':s.st_uid,'gid':s.st_gid,'xattrs':{n:os.getxattr(p,n).hex() for n in os.listxattr(p)}}
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NOATIME)
 try:
  import array
  flags=array.array('I',[0]);fcntl.ioctl(fd,0x80086601,flags,True);out['filesystem_flags']=flags[0];assert not flags[0] & (0x10|0x20),'Immutable/append-only entry requires review'
 finally:os.close(fd)
 return out

def processes():
 result=[]
 # Host PIDs/effective UID/GID provide namespace-aware permission evidence.
 for line in run(['docker','top','immich_server','-eo','pid,comm']).stdout.splitlines()[1:]:
  pid,name=line.split(None,1)
  if 'node' not in name.lower() and 'immich' not in name.lower():continue
  data={}
  for l in pathlib.Path('/proc',pid,'status').read_text().splitlines():
   if ':' in l:
    k,v=l.split(':',1)
    if k in ('Name','Uid','Gid','Groups','CapEff'):data[k]=v.strip()
  data['host_pid']=int(pid);data['uid_map']=pathlib.Path('/proc',pid,'uid_map').read_text().strip();result.append(data)
 assert result,'No Immich/node process identified';return result

def host_access(procs):
 results=[]
 for p in procs:
  uid=int(p['Uid'].split()[1]);gid=int(p['Gid'].split()[1]);groups=[int(x) for x in p['Groups'].split()]
  def drop():os.setgroups(groups);os.setgid(gid);os.setuid(uid)
  code="import os,sys; assert all(os.access(p,os.W_OK|os.X_OK,effective_ids=True) for p in sys.argv[1:])"
  child=subprocess.run([sys.executable,'-c',code,SOURCE,str(TEST_DIR)],preexec_fn=drop,capture_output=True,timeout=5)
  assert child.returncode==0,'Host directory access insufficient; no permission change authorized'
  results.append({'host_uid':uid,'host_gid':gid,'groups':groups,'directory_write_search_access':True})
 return results

def container_evidence(require_write):
 js="""const fs=require('fs');let nodes=[];for(const n of fs.readdirSync('/proc')){if(!/^\\d+$/.test(n))continue;try{let s=fs.readFileSync('/proc/'+n+'/status','utf8');if(!/^Name:\\s*(node|immich)/m.test(s))continue;let value=k=>s.match(new RegExp('^'+k+':\\\\s*(.*)$','m'))?.[1];nodes.push({pid:n,uid:value('Uid'),gid:value('Gid'),groups:value('Groups')});}catch{}}console.log(JSON.stringify({exec_uid:process.getuid(),exec_gid:process.getgid(),nodes,mounts:fs.readFileSync('/proc/self/mountinfo','utf8').split('\\n').filter(l=>l.split(' ')[4]==='/mnt/archive/bilder-og-video'||l.split(' ')[4]==='/data')}));"""
 # Simpler status parsing avoids differences in process-name formatting.
 js=js.replace("let value=k=>s.match(new RegExp('^'+k+':\\\\s*(.*)$','m'))?.[1];","let value=k=>s.split('\\n').find(l=>l.startsWith(k+':'))?.split(':').slice(1).join(':').trim();")
 out=json.loads(run(['docker','exec','immich_server','node','-e',js]).stdout)
 lib=[l for l in out['mounts'] if l.split()[4]==TARGET];assert len(lib)==1
 mode=lib[0].split()[5].split(',');assert ('rw' if require_write else 'ro') in mode
 assert out['nodes'],'No container node identity found'
 pairs={(int(p['uid'].split()[1]),int(p['gid'].split()[1])) for p in out['nodes']}
 for uid,gid in pairs:
  access="const f=require('fs');for(const p of process.argv.slice(1))f.accessSync(p,f.constants.R_OK|f.constants.X_OK"+ ('|f.constants.W_OK' if require_write else '')+");"
  run(['docker','exec','--user',f'{uid}:{gid}','immich_server','node','-e',access,TARGET,TARGET+'/Disposeable'])
 run(['docker','exec','immich_server','node','-e',"const f=require('fs');f.accessSync('/data',f.constants.R_OK|f.constants.W_OK|f.constants.X_OK);if(!f.statSync('/mnt/archive/bilder-og-video/Disposeable/Xenomorph.jpg').isFile())process.exit(1);"])
 out['directory_access_ok']=True;out['managed_storage_accessible']=True;return out

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--apply',action='store_true',required=True);ap.parse_args()
 assert os.geteuid()==0,'Run in an authenticated terminal with sudo; no password is stored'
 CONTROL.mkdir(parents=True,exist_ok=True)
 lock=(CONTROL/'apply.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 previous=CONTROL/'latest-result.json'
 if previous.exists():assert not json.loads(previous.read_text()).get('apply_attempted'),'Already applied/attempted; inspect existing receipt instead of rerunning'
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ');out=CONTROL/stamp;out.mkdir()
 report.update({'started_at':stamp,'evidence_directory':str(out),'compose_file':str(COMPOSE),'test_file':str(TEST_FILE)})
 def save():
  data=json.dumps(report,indent=2)+'\n';(out/'result.json').write_text(data);previous.write_text(data)
 try:
  assert run(['hostname']).stdout.strip()=='homelab'
  mount=json.loads(run(['findmnt','-J','-T',SOURCE,'-o','TARGET,SOURCE,FSTYPE,UUID']).stdout)['filesystems'][0]
  assert mount['target']=='/srv/storage' and mount['fstype']=='ext4' and mount['uuid']=='0cd558d4-359e-4dab-922c-68bfdd5db432';report['filesystem']=mount
  text=COMPOSE.read_text();assert hashlib.sha256(text.encode()).hexdigest()==EXPECTED_SHA,'Compose changed since preparation';assert text.count(OLD)==1;new=text.replace(OLD,NEW)
  beforeconfig=config(text);afterconfig=config(new);assert beforeconfig['name']=='immich'
  beforebind=[v for v in beforeconfig['services']['immich-server']['volumes'] if v['target']==TARGET];afterbind=[v for v in afterconfig['services']['immich-server']['volumes'] if v['target']==TARGET]
  assert len(beforebind)==len(afterbind)==1 and beforebind[0]['source']==afterbind[0]['source']==SOURCE
  assert beforebind[0].get('read_only') is True and not afterbind[0].get('read_only',False)
  expected=copy.deepcopy(beforeconfig)
  b=next(v for v in expected['services']['immich-server']['volumes'] if v['target']==TARGET)
  if 'read_only' in afterbind[0]:b['read_only']=afterbind[0]['read_only']
  else:b.pop('read_only',None)
  assert expected==afterconfig,'Unrelated rendered Compose change'
  live=inspect();assert healthy(live),'Pre-existing unhealthy stack; stop'
  for n,x in live.items():assert x['Config']['Labels']['com.docker.compose.project']=='immich'
  server=live['immich_server'];labels=server['Config']['Labels'];assert labels['com.docker.compose.project.working_dir']==str(COMPOSE.parent);assert labels['com.docker.compose.project.config_files']==str(COMPOSE)
  bind=[m for m in server['Mounts'] if m['Destination']==TARGET];assert len(bind)==1 and bind[0]['Source']==SOURCE and not bind[0]['RW']
  assert [m for m in server['Mounts'] if m['Source'].startswith('/srv/storage/archive')]==bind,'Unexpected broader archive mount'
  assert server['Config']['Image']==afterconfig['services']['immich-server']['image'];image=json.loads(run(['docker','image','inspect',server['Config']['Image']]).stdout)[0];assert image['Id']==server['Image'],'Local tag differs from running image; no upgrade authorized'
  procs=processes();report['before']={'containers':safe_summary(live),'processes':procs,'host_access':host_access(procs),'container':container_evidence(False),'http':http()}
  original={str(p):proof(p) for p in [pathlib.Path(SOURCE),TEST_DIR,TEST_FILE]};assert stat.S_ISREG(os.lstat(TEST_FILE).st_mode);report['before']['filesystem_evidence']=original
  # No archive payload is opened for content, written, created or deleted.
  backup=out/'docker-compose.yml.before';backup.write_bytes(text.encode());report['rollback_backup']=str(backup);report['rendered_diff_only_read_only_flag']=True;save()
  COMPOSE.write_text(new)
  dc('config','--quiet')
  report['apply_attempted']=True;save()
  dc('up','-d','--no-deps','--pull','never','immich-server');report['applied']=True;save()
  deadline=time.monotonic()+180
  while True:
   after=inspect()
   if healthy(after):break
   assert time.monotonic()<deadline,'Health timeout; inspect receipt and rollback if needed'
   print('Waiting for Immich health...',flush=True);time.sleep(5)
  assert after['immich_server']['Id']!=server['Id']
  for n in NAMES:
   assert after[n]['Image']==live[n]['Image']
   assert after[n]['HostConfig']['RestartPolicy']==live[n]['HostConfig']['RestartPolicy']
   if n!='immich_server':assert after[n]['Id']==live[n]['Id'] and after[n]['Mounts']==live[n]['Mounts']
  expectedmounts=copy.deepcopy(server['Mounts'])
  m=next(m for m in expectedmounts if m['Destination']==TARGET);m['RW']=True;m['Mode']='rw'
  assert after['immich_server']['Mounts']==expectedmounts,'Unrelated mount change'
  assert after['immich_server']['RestartCount']==0
  afterprocs=processes();report['after']={'containers':safe_summary(after),'processes':afterprocs,'host_access':host_access(afterprocs),'container':container_evidence(True),'http':http()}
  run(['docker','exec','immich_postgres','pg_isready']);report['after']['database_ready']=True
  log_result=run(['docker','logs','--since',after['immich_server']['State']['StartedAt'],'immich_server']);logs=log_result.stdout+'\n'+log_result.stderr
  # Raw logs/config/env are deliberately never persisted or printed.
  errors=re.findall(r'(?i)EACCES|EROFS|permission denied|read-only file system|fatal|panic|unhandled exception',logs)
  report['after']['startup_error_keywords']=dict((v,errors.count(v)) for v in set(errors));assert not errors,'Startup error keywords; review before declaring success'
  final={str(p):proof(p) for p in [pathlib.Path(SOURCE),TEST_DIR,TEST_FILE]}
  assert final[str(TEST_FILE)]==original[str(TEST_FILE)],'Disposable image metadata changed'
  assert final[str(TEST_DIR)]==original[str(TEST_DIR)],'Disposable folder metadata changed'
  report['after']['test_file_unchanged']=True;report['after']['test_file_exists']=True;report['after']['host_permissions_unchanged']=all(final[k]['mode']==original[k]['mode'] and final[k]['uid']==original[k]['uid'] and final[k]['gid']==original[k]['gid'] and final[k]['xattrs']==original[k]['xattrs'] for k in final);assert report['after']['host_permissions_unchanged']
  assert config(COMPOSE.read_text())==afterconfig
  report['success']=True;report['completed_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();save();print('PASS: archive bind RW; stack healthy; test image unchanged. Receipt: '+str(out/'result.json'))
 except Exception as exc:
  report['error']=str(exc)
  # A validation failure before application restores only our exact config bytes.
  if not report.get('apply_attempted') and 'new' in locals() and COMPOSE.read_text()==new:
   COMPOSE.write_text(text);report['pre_apply_config_restored']=True
  save();print('STOP: '+str(exc)+'; receipt '+str(out/'result.json'),file=sys.stderr);raise SystemExit(1)
if __name__=='__main__':main()
