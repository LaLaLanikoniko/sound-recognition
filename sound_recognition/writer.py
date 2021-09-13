def write(recognition_result, srt_file_path):
    with open(srt_file_path, "a", encoding='UTF-8') as f:
        for i, result in enumerate(recognition_result):

            start_time = str(result["start_time"])
            end_time = str(result["end_time"])

            f.write(str(i + 1) + "\n")
            f.write(process_time_str(start_time) + " --> " + process_time_str(end_time) + "\n")
            f.write(result["script"] + "\n")
            f.write('\n')


def process_time_str(time_str):
    if "." in time_str:
        time_str = time_str[:: -1].replace(".", ",")
        time_str = time_str[:: -1]
        time_str = time_str[:-3]
    else:
        time_str += ",000"

    return time_str

