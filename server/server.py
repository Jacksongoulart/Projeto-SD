import signal  # Signal support (server shutdown on signal receive)
import argparse
import pythonserver
import sys
import socket
sys.path.append('../client/')
import pythonclient
import get_ip

def graceful_shutdown(sig, dummy):
    s.shutdown()

def get_parameters():
    parser = argparse.ArgumentParser(description='Http Server')
    parser.add_argument('path', metavar='path', type=str,
                       help='The folder to be downloaded by the clients')
    parser.add_argument('port', metavar='port', type=int,
                       help='The port for the server to listen')
    parser.add_argument('loadBalancer', metavar='loadbalancer', type=str,
                   	   help='IP:port of the Load Balancer')
    return parser.parse_args()

signal.signal(signal.SIGINT, graceful_shutdown)
args = get_parameters()
print "Starting web server"
s = pythonserver.PythonServer(args.port, args.path)
sign = args.loadBalancer + '/cadastro?ip=' + get_ip.get_lan_ip() + '&port=' + str(args.port)
print sign
pythonclient.client(sign)
s.activate_server()
s.wait_for_connections()