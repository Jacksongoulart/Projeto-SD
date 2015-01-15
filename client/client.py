import pythonclient
import argparse

def get_parameters():
    parser = argparse.ArgumentParser(description='Http Client')
    parser.add_argument('request', metavar='request', type=str,
                       help='...')
    return parser.parse_args()

args = get_parameters()
print "Inicio..."
print pythonclient.client(args.request)