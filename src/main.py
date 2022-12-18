import json
import os

from functions import arguments, helpers

args = arguments.handleArgs()

# Secrets
# ====================================================================================
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

# Initialization
# ====================================================================================
helpers.checkInstalledPackages()

config = helpers.read_json(f'configs/{args.file}')['client']

logger = helpers.log(args)

# Debug - Display Config Dictionary
logger.debug(json.dumps(config, indent=4))

def main():
    pass

if __name__ == '__main__':
    main()