import json
import os
import csv
import statistics

# with open('test.json', 'r') as read_file:
#     data = json.load(read_file)

metrics = ["first-contentful-paint", "largest-contentful-paint", "speed-index", "total-blocking-time", 
           "cumulative-layout-shift", "interactive", "network-requests", "server-response-time"]

actual_metrics = ["first-contentful-paint", "largest-contentful-paint", "speed-index", "total-blocking-time", 
           "cumulative-layout-shift", "interactive", "transfer-size", "resource-size", "server-response-time"]

# additional_metrics = ["transfer-size", "resource-size"]
metric_results = {metric: 0 for metric in actual_metrics}
counts_accumulator = {metric: 0 for metric in actual_metrics}

# Open the CSV file in write mode and write the header
with open('extracted_data.csv', mode='w', newline='') as csvfile:
    fieldnames = ['Metric', 'Value']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

def data_processing(metric):
    if metric in data["audits"]:
        if metric == "network-requests":
            print('network-requests is found')
            metric_js_bundle = data["audits"][metric]
            if "items" in metric_js_bundle["details"]:
                print('network-requests items is found')
                items_metric_js_bundle = metric_js_bundle["details"]["items"]
                url_found = False
                for item in items_metric_js_bundle:
                    if "bundle.js" in item.get("url"):
                        print('JS bundle is found')
                        transfer_size = item.get("transferSize")
                        resource_size = item.get("resourceSize")
                        url_found = True

                        if transfer_size is not None and resource_size is not None:
                            metric_results["transfer-size"] += transfer_size
                            metric_results["resource-size"] += resource_size
                            counts_accumulator["transfer-size"] += 1
                            counts_accumulator["resource-size"] += 1

                            # Write to the CSV file
                            with open('extracted_data.csv', mode='a', newline='') as csvfile:
                                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                writer.writerow({'Metric': 'transfer-size', 'Value': transfer_size})
                                writer.writerow({'Metric': 'resource-size', 'Value': resource_size})

                            print(f'Transfer size: {transfer_size}')
                            print(f'Resource size: {resource_size}')
                            break
                        else:
                            print('Transfer size and Resource size not found')
                            break
                if not url_found:
                    print(f'JS bundle not found')
            else:
                print(f'Items key not found inside network-requests')
        else: 
            metric_data = data["audits"][metric]
            numeric_value = metric_data.get('numericValue')
            if numeric_value is not None:
                metric_results[metric] += numeric_value
                counts_accumulator[metric] += 1

                # Write to the CSV file
                with open('extracted_data.csv', mode='a', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow({'Metric': metric, 'Value': numeric_value})

                print(f'{metric}: {numeric_value} milliseconds')
            else:
                print(f'{metric} numeric value not found inside audits data')
    else:
        print(f'{metric} not found inside audits data structure')



if __name__ == "__main__":
    for filename in os.listdir(r"D:\ITU\ResearchProject\React\my-app\5runs"):
        if filename.endswith(".json"):
            with open(os.path.join(r"D:\ITU\ResearchProject\React\my-app\5runs", filename), "r") as read_results:
                data = json.load(read_results)

            for metric in metrics:
                data_processing(metric)

    
