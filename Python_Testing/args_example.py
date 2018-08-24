import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-ttl",help="Time to log",type=int,default=5)
parser.add_argument("-comment",help="Comment",default="Test")

args = parser.parse_args()

print(args.ttl)
print (args.comment)
