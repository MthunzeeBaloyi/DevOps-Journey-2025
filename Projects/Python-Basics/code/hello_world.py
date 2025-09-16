# hello_world.py
# Simple script used during the Python Basics course

def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', default='Solomon', help='Name to greet')
    args = parser.parse_args()
    print(greet(args.name))
