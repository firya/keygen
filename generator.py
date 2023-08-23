import itertools
import pymorphy2
import time

class Generator:
    columns = ()
    columns_count = 0
    props = ()
    morph = pymorphy2.MorphAnalyzer()
    cluster_iteration = 0
    prev_cluster_result = []
    cartesian_max = 100000
    priority_list = []

    max_key_length = 7
    stop_words = ["а","будем","будет","будешь","буду","будут","будь","будьте","бы","был","была","были","было","быть","в","вам","вами","вас","весь","во","вот","все","всего","всей","всем","всеми","всему","всех","всею","всю","вся","вы","да","для","до","его","ее","ей","ему","если","есть","еще","ею","же","за","и","из","или","им","ими","их","к","как","кем","ко","когда","кого","ком","кому","которая","которое","которо","которо","которо","которо","которо","которую","которые","который","которы","которы","которы","кто","меня","мне","мной","мною","мог","моги","могите","могла","могли","могло","могу","могут","мое","моего","моей","моем","моему","моею","можем","может","можете","можешь","мои","моим","моими","моих","мой","мочь","мою","моя","мы","на","нам","нами","нас","наш","наша","наше","нашего","нашей","нашем","нашему","нашею","наши","нашим","нашими","наших","нашу","не","него","нее","ней","нем","нему","нет","нею","ним","ними","них","но","о","об","один","одна","одни","одним","одними","одних","одно","одного","одной","одном","одному","одною","одну","он","она","они","оно","от","по","при","с","сам","свое","своего","своей","своем","своему","своею","свои","своим","своими","своих","свой","свою","своя","себе","себя","собой","собою","та","так","такая","такие","таким","такими","таких","такого","такое","такой","таком","такому","такою","такую","те","тебе","тебя","тем","теми","тех","то","тобой","тобою","того","той","только","том","тому","тот","ту","ты","у","уже","чего","чем","чему","что","чтобы","эта","эти","этим","этими","этих","это","этого","этой","этом","этому","этот","эту","я","a","about","all","an","and","any","are","as","at","be","but","by","can","do","for","from","have","her","i","if","in","is","it","my","no","not","of","on","one","or","so","that","the","there","they","this","to","was","we","what","which","will","with","would","you"];

    def __init__(self, params):
        self.columns = params['columns']
        self.columns_count = len(self.columns)
        self.props = params['props']

    def generate(self):
        start_time = time.time()

        if self.props['match_words']:
            self.find_match_words()
        
        result = {}

        if self.props['cluster']:
            self.get_priority_list()

            result = self.groups_to_table(self.clusterisation2())
        else:
            cartesian_list = []
            for column in self.columns:
                cartesian_list.append(column['data'])

            cartesian = self.cartesian_product(cartesian_list)

            keywords = []
            for row in cartesian:
                keywords.append(self.format_result(self.match_words(row), True))

            result = {
                "keywords": keywords
            }

        result['gen_time'] = "%s seconds" % (time.time() - start_time)

        print(result['gen_time'])

        return result

    def clusterisation2(self):
        result = []

        groups = [[''] for i in range(len(self.columns))]

        group_columns = self.group_columns()

        for group in group_columns:
            groups[group] = self.columns[group]['data']

        groups = self.cartesian_product(groups)

        result.append({
            "group_name": ["Шаблон"],
            "headers": ['']*len(self.props['headers']),
            "keywords": []
        })

        for group in groups:
            group_name = self.generate_header(group, self.priority_list, 0)

            headers = []
            for header_len in self.props['headers']:
                if header_len > 0:
                    headers.append(self.generate_header(group, self.priority_list, header_len, self.merge_lists(headers)))

            keywords = []
            cartesian_list = [[''] for i in range(len(self.columns))]
            for i, column in enumerate(group):
                if i in group_columns:
                    cartesian_list[i][0] = column
                else:
                    cartesian_list[i] = self.columns[i]['data']

            keywords = self.cartesian_product(cartesian_list)

            keywords_to_add = []

            for keyword in keywords:
                if self.count_length(self.match_words(keyword)) <= self.props['headers'][0]:
                    result[0]['keywords'].append(keyword)
                else: 
                    keywords_to_add.append(keyword)

            result.append({
                "group_name": group_name,
                "headers": headers,
                "keywords": keywords_to_add
            })

        return result

    def group_columns(self):
        group_columns = []
        total_groups = 1
        group_max_length = sum(self.props['headers'])
        # Минимальная длна заголовка кроме 0
        min_length = min(i for i in self.props['headers'] if i > 0)

        max_header = ['']*len(self.columns)

        for priority_item in self.priority_list:
            total_groups_temp = total_groups*len(self.columns[priority_item[0]]['data'])
            
            if total_groups_temp < self.props['clusterCount']:
                # Найдем самое длинное значение
                word = max(self.columns[priority_item[0]]['data'], key=len)

                max_header[priority_item[0]] = word

                max_header_len = self.count_length(self.generate_header(max_header, self.priority_list, group_max_length))

                if max_header_len <= group_max_length and len(word) <= min_length:
                    group_columns.append(priority_item[0])
                    total_groups = total_groups_temp
                else:
                    max_header[priority_item[0]] = ''

        return group_columns

    def groups_to_table(self, groups):
        table = []

        row = ["Название группы", "Ключевое слово"]
        for i in range(len(self.props['headers'])):
            if self.props['headers'][i] > 0:
                row.append(f"Заголовок {(i+1)}")

        table.append(row)

        for i, group in enumerate(groups):
            for keyword in group['keywords']:
                row = []

                row.append(self.format_result(self.match_words(group['group_name'])))

                row.append(self.format_result(self.match_words(keyword), True))

                for j, header in enumerate(group['headers']):
                    if self.props['headers'][j] > 0:
                        row.append(self.format_result(self.match_words(header)))

                table.append(row)

        return {
            "table": table,
            "num_groups": len(groups)
        }

    def generate_header(self, words, priority, max_length, exclude=[]):
        header = ['']*len(words)
        
        for priority_item in priority:
            if (self.count_length(header) + len(words[priority_item[0]]) + 1 <= max_length and max_length > 0) or max_length == 0:
                if (len(exclude) == 0) or (len(exclude) > 0 and exclude[priority_item[0]] == ''):
                    header[priority_item[0]] = words[priority_item[0]]

        if self.props['match_words']:
            header_matched = self.match_words(header)
            header_len = self.count_length(header_matched)

            if header_len > max_length and max_length > 0:
                return self.generate_header(words, priority, max_length - 1, exclude)

        return header

    def merge_lists(self, lists):
        result = []

        if len(lists):
            result = lists[0].copy()

            for i, el in enumerate(result):
                for list in lists:
                    if list[i] != '':
                        result[i] = list[i]
                        break
            
        return result

    def count_length(self, array):
        length = 0

        for i, el in enumerate(array):
            if el:
                if length > 0:
                    length += 1
                length = length + len(el)

        return length
            

    def get_priority_list(self):
        priority = []

        for i, column in enumerate(self.columns):
            priority.append([i, column['priority']])

        priority = sorted(priority, key=lambda p: float(p[1]), reverse=True)

        self.priority_list = priority

    def find_match_words(self):
        for i, column in enumerate(self.columns):
            if len(column['decl']):
                for j, decl in enumerate(column['decl']):
                    decl_result = []
                    self.columns[i]['decl'][j]['result'] = {}

                    for el in column['data']:
                        needed_form = self.morph.parse(decl['form'])[0]

                        needed_tag = {needed_form.tag.case,
                                    needed_form.tag.number}

                        result = []
                        words = el.split(" ")
                        for word in words:
                            p = self.morph.parse(word)[0]
                            p = p.inflect(needed_tag)
                            
                            if p!=None:
                                result.append(p.word)
                            else:
                                result.append(word)

                        decl_result.append(" ".join(result))

                    self.columns[i]['decl'][j]['result'] = decl_result

    def match_words(self, array):
        matched_list = []

        for i, col in enumerate(array):
            if col != '' and len(self.columns[i]['decl']) > 0:
                list_item_col = ""
                for decl in self.columns[i]['decl']:
                    if decl['word'] == array[decl['col']]:
                        list_item_col = matched_list.append(decl['result'][self.columns[i]['data'].index(col)])

                if list_item_col=="":
                    matched_list.append(col)
            else:
                matched_list.append(col)

        return matched_list

    def cartesian_product(self, cartesian_list):
        c_product = []

        for element in itertools.product(*cartesian_list):
            if (self.props['maxKeyLength'] and self.word_count(element) <= self.max_key_length) or not self.props['maxKeyLength']:
                c_product.append(element)

        return c_product

    def cartesian_product_count(self, columns):
        result = 1

        for column in columns:
            result = result * len(column['data'])

        return result

    def word_count(self, el):
        word_arr = self.split_by_word(el)
        
        if not self.props['plus']:
            for word in word_arr:
                if word in self.stop_words:
                    word_arr.remove(word)

        return len(word_arr)

    def split_by_word(self, el):
        word_arr = []
        el = filter(None, el)

        for col in el:
            words = col.split(" ")
            for word in words:
                word_arr.append(word)
            
        return word_arr

    def format_result(self, el, plus=False):
        result = ""

        if len(el):
            words = self.split_by_word(el)
            if plus and self.props['plus']:
                words = self.add_stop_word_plus(words)

            words = list(filter(None, words))

            if len(words):
                words[0] = words[0][:1].upper() + words[0][1:]

            result = " ".join(words)
        
        return result

    def add_stop_word_plus(self, words):
        result = []

        for word in words:
            if word in self.stop_words:
                result.append("+"+word)
            else:
                result.append(word)

        return result