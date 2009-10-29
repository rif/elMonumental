from fabric.api import hosts, prompt, sudo, run, local, cd

def ci():
    """Commit localy using mercurial"""
    comment = prompt('Commit comment: ', default='another commit from fabric')
    local('hg ci -m "%s"' % comment)
    local('hg push')

@hosts('root@10.40.8.206')
def deploy():
    'Deploy the app to the target environment'
    with cd('/var/django/elMonumental/'):
        run('hg pul -uv')
        run('touch ./apache/django.wsgi')
    
