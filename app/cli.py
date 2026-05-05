import argparse
from dataclasses import replace

from app.config import Settings
from app.demo_server import run as serve
from app.scraper import run_scrape


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='cmd', required=True)
    a = sub.add_parser('serve-demo')
    a.add_argument('--host', default='127.0.0.1')
    a.add_argument('--port', type=int, default=5000)
    b = sub.add_parser('scrape')
    b.add_argument('--base-url')
    b.add_argument('--output-dir')
    args = parser.parse_args()
    if args.cmd == 'serve-demo':
        serve(args.host, args.port)
    if args.cmd == 'scrape':
        s = Settings()
        if args.base_url:
            s = replace(s, base_url=args.base_url)
        if args.output_dir:
            s = replace(s, output_dir=args.output_dir)
        print(run_scrape(s))


if __name__ == '__main__':
    main()
