# This one-day project is an attempt to analyze the balance of Enlisted game mode
# The resulting data can be found in the [output](https://github.com/rurikrok/enlisted-balance/tree/master/output) folder or [output.zip](https://github.com/rurikrok/enlisted-balance/tree/master/output.zip) file

## The workflow is as follows:

1. Data on the number of reinforcements (score_cap), capture time (cap_time), and the number of reinforcements for capturing zones (cap_reward) were collected from the invasion mode map files. The data is available in JSON format [data.json](https://github.com/username/repository/tree/master/output/data.json) and Excel format [data.xlsx](https://github.com/username/repository/tree/master/output/data.xlsx)

2. Next, the average values of the number of reinforcements (score_cap), capture time (cap_time), and the number of reinforcements for capturing zones (cap_reward) are calculated for each campaign and faction. The data is available in the TXT file format [average.txt](https://github.com/username/repository/tree/master/output/average.txt)

3. To visualize the average values data, graphs are created based on these data. The files can be found in the [output/charts](https://github.com/rurikrok/enlisted-balance/tree/master/output/charts) folder

4. In order to conduct an honest balance analysis, "paired" maps are searched for - differing only in the attacking faction. Text files with the resulting average values and graphs can be found in the [output/pair_maps](https://github.com/rurikrok/enlisted-balance/tree/master/output/pair_maps) folder

# Этот однодневный проект - попытка проанализировать баланс Enlisted
# Полученные данные можно посмотреть в папке  [output](https://github.com/rurikrok/enlisted-balance/tree/master/output) или скачать архивом [output.zip](https://github.com/rurikrok/enlisted-balance/tree/master/output.zip)

## Логика работы:

1. Из файлов карт режима вторжения собраны данные о количестве подкреплений (score_cap), времени захвата зон (cap_time) и количества подкреплений за захват зон (cap_reward).
Эти данные доступны в виде json-файла [data.json](https://github.com/username/repository/tree/master/output/data.json) и excel-файла [data.xlsx](https://github.com/username/repository/tree/master/output/data.xlsx)

2. Далее для каждой кампании и стороны вычисляются средние значения количества подкреплений (score_cap), времени захвата зон (cap_time) и количества подкреплений за захват зон (cap_reward).
Эти данные доступны в виде txt-файла [average.txt](https://github.com/username/repository/tree/master/output/average.txt) 

3. Для наглядности на основе данных о средних значениях строятся графики. Файлы лежат в папке [output/charts](https://github.com/rurikrok/enlisted-balance/tree/master/output/charts)

4. Для честного анализа баланса ищутся "парные" карты - отличающиеся только атакующей стороной. Текстовые файлы с полученными средними значениями и графики лежат в папке [output/pair_maps](https://github.com/rurikrok/enlisted-balance/tree/master/output/pair_maps)