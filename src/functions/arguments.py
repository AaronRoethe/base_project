import argparse

def handleArgs():
    parser = argparse.ArgumentParser(description='fillme')
    parser.add_argument("-v", "--verbose", help="Displays Detailed Information", action="store_true")
    parser.add_argument("-d", "--deployEnvironment", help="Deploys Datastore to Environment", choices=['ag1', 'us2', 'us1'])
    parser.add_argument("-f", "--file", help="Input JSON File", required=True )
    parser.add_argument("--dryrun", action="store_true")

    return parser.parse_args()