from fabric.api import hosts, prompt, sudo, local, cd

def ci():
    """Commit localy using mercurial"""
    comment = prompt('Commit comment: ', default='another commit from fabric')
    local('hg ci -m "%s"' % comment)
    local('hg push')

@hosts('10.40.8.206')
def deploy():
    'Deploy the app to the target environment'
    with cd('/var/django/elMonumental/'):
        sudo('hg pul -uv')
        sudo('touch ./apache/django.wsgi')
    
