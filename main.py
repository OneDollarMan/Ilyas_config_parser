import argparse
import os


def find_word_occurrences(settings_file, config_file, result_file):
    # Чтение слов из файла settings.txt
    with open(settings_file, 'r', encoding='utf-8') as settings:
        keywords = [line.strip() for line in settings if line.strip()]

    # Открываем файл config.txt и result.txt
    with open(config_file, 'r', encoding='utf-8') as config, open(result_file, 'w', encoding='utf-8') as result:
        # Проходим по каждой строке конфигурационного файла
        interface_name = None
        for line in config:
            if 'interface' in line:
                interface_name = line
            if '!' in line:
                interface_name = None

            # Проверяем, содержится ли какое-либо из ключевых слов в строке
            if any(keyword in line for keyword in keywords):
                # Записываем строку в файл result.txt
                if interface_name:
                    result.write(f'[{interface_name.strip()}]: {line}')
                else:
                    result.write(f'[no interface]: {line}')


def parse_args(input_args=None):
    parser = argparse.ArgumentParser(description="Simple example of a training script.")
    parser.add_argument(
        "--config_dir",
        type=str,
        default=None,
        required=False,
        help="Path to dir with configs",
    )

    if input_args is not None:
        args = parser.parse_args(input_args)
    else:
        args = parser.parse_args()

    return args


def process_txt_files_in_directory(settings_file, directory, result_directory):
    # Ищем все .txt файлы в указанной директории
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            config_file = os.path.join(directory, filename)
            result_file = os.path.join(result_directory, f"result_{filename}")
            print(f"Processing file: {config_file} -> {result_file}")
            # Вызываем find_word_occurrences для каждого .txt файла
            find_word_occurrences(settings_file, config_file, result_file)


def main(args):
    settings_file = 'settings.txt'
    result_directory = 'result'
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)

    process_txt_files_in_directory(settings_file, args.config_dir, result_directory)


if __name__ == '__main__':
    args = parse_args()
    main(args)
