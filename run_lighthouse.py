import subprocess
import concurrent.futures
import argparse
import os

def run_lighthouse(index, target_url, output_directory):
    output_path = os.path.join(output_directory, f'lighthouse_report_{index}.json')
    lighthouse_command = (
        f'lighthouse {target_url} --only-categories=performance --output json '
        f'--output-path "{output_path}" --chrome-flags="--headless"'
    )
    subprocess.run(lighthouse_command, shell=True)

def run_concurrently(num_runs, target_url, output_directory):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(run_lighthouse, i, target_url, output_directory) for i in range(1, num_runs + 1)]

        # wait for all futures to complete
        concurrent.futures.wait(futures)

    print("Lighthouse test(s) completed.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Lighthouse tests concurrently.')
    parser.add_argument('--n', type=int, default=1, help='Number of times to run the Lighthouse command')
    parser.add_argument('--url', type=str, default='', help='Target URL for Lighthouse test')
    parser.add_argument('--output', type=str, default='', help='Output directory for Lighthouse reports')

    args = parser.parse_args()

    run_concurrently(args.n, args.url, args.output)
