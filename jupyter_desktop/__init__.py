import os
import shlex
import tempfile


HERE = os.path.dirname(os.path.abspath(__file__))

def setup_desktop():
    # make a secure temporary directory for sockets
    # This is only readable, writeable & searchable by our uid
    sockets_dir = tempfile.mkdtemp()
    sockets_path = os.path.join(sockets_dir, 'vnc-socket')

    vnc_command = ' '.join((shlex.quote(p) for p in [
        'vncserver',
        '-verbose',
        '-xstartup', os.path.join(HERE, 'share/xstartup'),
        '-SecurityTypes', 'None',
        '-rfbunixpath', sockets_path,
        '-fg',
        '-nolisten',
        'tcp',
    ]))
    return {
        'command': [
            'websockify', '-v',
            '--web', os.path.join(HERE, 'share/web/noVNC-1.1.0'),
            '--heartbeat', '30',
            '--unix-target', sockets_path,
            '{port}',
            '--',
            '/bin/sh', '-c',
            f'cd {os.environ["HOME"]} && {vnc_command}'
        ],
        'timeout': 30,
        'mappath': {'/': '/vnc_lite.html'},
    }
