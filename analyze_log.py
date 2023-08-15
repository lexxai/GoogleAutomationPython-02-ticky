#!/usr/bin/env python3

import sys
import re
import csv
import operator


def to_csv(data, filename, fields):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fields)
        writer.writerows(data)


def to_csv_dict(data, filename, fields):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fields)
        for item in data:
            row = []
            row.append(item[0])
            row.append(item[1].get("INFO", 0))
            row.append(item[1].get("ERROR", 0))
            writer.writerow(row)
            # print(f"{row=}")


def analyze_log(log_file: str, service_name: str = "ticky"):
    user_count = {}
    user_events = {}
    bad_event_count = {}
    with open(log_file, "r") as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            if service_name in line:
                # print(f"{line=}")
                pattern_username = r"\s.+:\s([A-Z]+).+\((.+)\)$"
                result = re.search(pattern_username, line)
                if result:
                    error_type = result[1]
                    # print(f"{error_type=}")
                    user = result[2]

                    # count types of user messages
                    event = user_events.get(user, {})
                    event_cnt = event.get(error_type, 0)
                    event[error_type] = event_cnt + 1
                    user_events[user] = event

                    # count users
                    n = user_count.get(user, 0) + 1
                    user_count[user] = n

                pattern_error = r"ERROR\s(.+)\s\(.+\)$"
                result = re.search(pattern_error, line)
                if result:
                    error = result[1].strip()
                    n = bad_event_count.get(error, 0) + 1
                    bad_event_count[error] = n

    # user_count_sorted = sorted(user_count.items())

    user_count_sorted = sorted(user_count.items(), key=operator.itemgetter(0))

    # print(f"{user_count=}")
    # print(f"{user_count_sorted=}")
    # print(f"{user_events=}")
    # print(f"{user_events.items()=}")

    # user_events_sored = sorted(user_events.items())

    user_events_sored = sorted(user_events.items(), key=operator.itemgetter(0))

    # print(f"{user_events_sored=}")

    to_csv_dict(user_events_sored, "user_statistics.csv", ("Username", "INFO", "ERROR"))

    to_csv(user_count_sorted, "user.csv", ("User", "Count"))

    # bad_event_count_sorted = sorted(
    #     bad_event_count.items(), key=lambda x: x[1], reverse=True
    # )

    bad_event_count_sorted = sorted(
        bad_event_count.items(), key=operator.itemgetter(1), reverse=True
    )

    # print(f"{bad_event_count=}")
    # print(f"{bad_event_count_sorted=}")

    to_csv(bad_event_count_sorted, "error_message.csv", ("Error", "Count"))


if __name__ == "__main__":
    try:
        analyze_log(sys.argv[1])
    except IndexError:
        print("Log file not defied, please use path to log file as parameter")
