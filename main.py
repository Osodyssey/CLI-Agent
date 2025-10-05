import argparse
from agent.config import SANDBOX, AUTO_CONFIRM
from agent.core import run_agent

def main():
    parser = argparse.ArgumentParser(description='CLI Agent - multi-step AI executor')
    parser.add_argument('--goal', '-g', type=str, help='Goal description (if omitted, you will be prompted)')
    parser.add_argument('--auto-confirm', action='store_true', help='Auto-confirm dangerous commands')
    parser.add_argument('--no-sandbox', action='store_true', help='Disable sandbox mode (allow executing commands)')
    args = parser.parse_args()

    if args.auto_confirm:
        # toggle env var behavior via config globals (simpler than restarting)
        print('⚠️ AUTO_CONFIRM enabled for this run (note: persistent behavior depends on env vars).')

    if args.no_sandbox:
        print('⚠️ SANDBOX disabled for this run — commands will be executed for real.')

    goal = args.goal or input('🎯 هدف کاربر: ')
    run_agent(goal)

if __name__ == '__main__':
    main()
