from word_translate import WordTranslate
from word_to_phrase import WordToPhrase
import os


def scan(name,  # The words source.
         is_check_phrase=False,  # if check phrase
         rebuild=False):  # if need rebuild
    buffer = []
    if not rebuild:
        with open(f'{os.getcwd()}/output.log', 'r') as l:
            buffer = [line.replace('\n', '') for line in l.readlines()]

    base_path = f'{os.getcwd()}/paper'
    with open(f'{base_path}/{name}.txt', 'r') as r, open(f'{base_path}/output/{name}.md', 'a+') as w:
        for word in r.readlines():
            print('*'*20)
            word = word.replace('\n', '')
            if word in buffer:
                print(f'已处理: {word}')
                continue
            print(f'正在处理: {word}')

            # word
            wt = WordTranslate(word)
            detail = wt.run()
            if detail and len(detail.keys()):

                w.writelines("""
| 名称 | 英标 | 美标 |
| ---  | --- | --- |
| **{}**| `/{}/` | `/{}/` |\n
                """.format(word, detail["phonetics"]["uk"], detail["phonetics"]["us"]))

                for explain in detail["explains"]:
                    w.writelines("""
> {}  """.format(explain))

                w.writelines("\n")

                if is_check_phrase:
                    # phrase
                    wtp = WordToPhrase(word)
                    phrase = wtp.run()
                    if phrase and len(phrase.keys()):
                        index = 0
                        for k, v in phrase.items():
                            w.writelines("""
{}. **{}** {}  """.format(index, k, v))

                            index += 1

                w.writelines("""
                
-------\n\n
                """)

            buffer.append(word)

    with open(f'{os.getcwd()}/output.log', 'a+') as l:
        for word in buffer:
            l.writelines(f'{word}\n')


if __name__ == '__main__':
    try:
        scan('top-3000', is_check_phrase=False, rebuild=True)
    except Exception as e:
        print(e)
