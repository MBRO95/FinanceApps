if __name__ == "__main__":
  import argparse
  import subprocess
  parser = argparse.ArgumentParser(description='Financial Apps')
  apps = ["TLH","REBAL","ROI"]
  parser.add_argument('-a', '--application', nargs=1, choices=apps)
  args = parser.parse_args()
  if args.application == None:
    print("Please specify the app you'd like to launch with -a or --application")
    exit()
  elif args.application[0] == "TLH":
    subprocess.call("python " + args.application[0] + "/main.py -h", shell=True)
    print()
    security = input('Enter the security from the list above to evaluate: ')
    subprocess.call("python " + args.application[0] + "/main.py -s " + security, shell=True)
  else:
    subprocess.call("python " + args.application[0] + "/main.py", shell=True)