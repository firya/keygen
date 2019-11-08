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
        cartesian = self.cartesian_product()

        if self.props['match_words']:
            self.find_match_words()
        
        result = {}

        if self.props['cluster']:
            result = self.groups_to_table(self.clusterisation(cartesian))
        else:
            keywords = []
            for row in cartesian:
                keywords.append(self.format_result(self.match_words(row), True))

            result = {
                "keywords": keywords
            }

        result['gen_time'] = "%s seconds" % (time.time() - start_time)

        print(result['gen_time'])

        return result

    def clusterisation(self, cartesian, h1_len=None, num_headers=1):
        max_cluster_count = self.props['clusterCount'] if self.props['clusterCount'] else self.cartesian_max

        if h1_len is None:
            h1_len = self.props['headers'][0]

        self.cluster_iteration = self.cluster_iteration + 1

        groups = []
        default_group = []

        self.get_priority_list()

        for i, el in enumerate(cartesian):
            if self.count_length(el) <= self.props['headers'][0]:
                default_group.append({
                    "keyword": el,
                    "headers": [[] for i in range(num_headers)]
                })
            else:
                headers = []
                for i in range(0, num_headers):
                    headers.append(self.generate_header(el, self.priority_list, h1_len, self.merge_lists(headers)))
                
                if len(groups) > max_cluster_count:
                    group_n = self.find_group(groups, headers, num_headers)
                else:
                    group_n = len(groups)
                    
                    # Перегенерировать кластеры с меньшей длиной первого заголовка
                    if group_n >= max_cluster_count - 1 and i != len(cartesian) - 1 and num_headers == 1:
                        return self.clusterisation(cartesian, h1_len - 1)

                if group_n >= len(groups):
                        groups.insert(group_n, [])

                groups[group_n].append({
                    "keyword": el,
                    "headers": headers
                })

        groups.insert(0, default_group)

        groups = self.format_groups(groups, num_headers)

        if len(groups) > max_cluster_count and num_headers > 1:
            return self.prev_cluster_result

        self.prev_cluster_result = groups

        if len(groups) < max_cluster_count and num_headers < 3:
            return self.clusterisation(cartesian, h1_len, num_headers+1)

        return groups

    # Форматирует итоговые группы таким образом чтобы в структуре осталось по одному экземпляру заголовоков
    def format_groups(self, groups, num_headers):
        new_groups = []

        for group in groups:
            if len(group):
                new_group = {"headers": [], "keywords": []}
                group_headers = []
                group_keywords = []
                default_group = False

                for i in range(0, num_headers):
                    group_headers.append(group[0]['headers'][i])
                    if not len(group[0]['headers'][i]):
                        default_group = True 

                for el in group:
                    group_keywords.append(el['keyword'])
                
                if not default_group:
                    group_headers = group_headers + self.genereate_other_headers(group_keywords, group_headers)
                else:
                    for i in range(len(group_headers), len(self.props['headers'])):
                        group_headers.append("")
                
                for header in group_headers:
                    if self.props['match_words']:
                        new_group['headers'].append(self.format_result(self.match_words(header)))
                    else:
                        new_group['headers'].append(self.format_result(header))

                for keyword in group_keywords:
                    if self.props['match_words']:
                        new_group['keywords'].append(self.format_result(self.match_words(keyword), True))
                    else:
                        new_group['keywords'].append(self.format_result(keyword, True))

                new_groups.append(new_group)

        return new_groups

    def groups_to_table(self, groups):
        table = []

        row = ["Группа", "Ключевое слово"]
        for i in range(len(self.props['headers'])):
            if self.props['headers'][i] > 0:
                row.append(f"Заголовок {(i+1)}")

        table.append(row)

        for i, group in enumerate(groups):
            for keyword in group['keywords']:
                row = []

                row.append(f"Группа №{i+1}")

                row.append(keyword)

                for j, header in enumerate(group['headers']):
                    if self.props['headers'][j] > 0:
                        row.append(header)

                table.append(row)

        return {
            "table": table,
            "num_groups": len(groups)
        }

    def genereate_other_headers(self, keywords, headers):
        result = []

        not_used_keywords = [{} for i in range(self.columns_count)]

        for keyword in keywords:
            for i, word in enumerate(keyword):
                if word != '':
                    for header in headers:
                        if len(header):
                            if header[i] == word:
                                break
                    else:
                        if word in not_used_keywords[i]:
                            not_used_keywords[i][word] = not_used_keywords[i][word] + 1
                        else:
                            not_used_keywords[i][word] = 1

        for i in range(len(headers), len(self.props['headers'])):
            result_item = [""]*self.columns_count

            for j, keyword in enumerate(not_used_keywords):
                keyword_max_len = 0

                for key, value in keyword.items():
                    if value > keyword_max_len:
                        result_item[j] = key
                        keyword_max_len = value

            for k, word in enumerate(result_item):
                if word != '':
                    del not_used_keywords[k][word]

            result.append(self.generate_header(result_item, self.priority_list, self.props['headers'][i]))
                
        return result

    def find_group(self, groups, headers, num):
        result = len(groups)
        
        for j, group in enumerate(groups):
            for el in group:
                for i in range(num):
                    if el['headers'][i] != headers[i]:
                        break
                else: 
                    result = j
                    break

        return result

    def generate_header(self, words, priority, max_length, exclude=[]):
        header = ['']*len(words)
        
        for priority_item in priority:
            if self.count_length(header) + len(words[priority_item[0]]) + 1 <= max_length:
                if (len(exclude) == 0) or (len(exclude) > 0 and exclude[priority_item[0]] == ''):
                    header[priority_item[0]] = words[priority_item[0]]

        if self.props['match_words']:
            header_matched = self.match_words(header)
            header_len = self.count_length(header_matched)

            if header_len > max_length:
                self.generate_header(words, priority, max_length - 1, exclude)

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
                if i > 0:
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

    def cartesian_product(self):
        list = []
        for column in self.columns:
            list.append(column['data'])

        c_product = []

        for element in itertools.product(*list):
            if (self.props['maxKeyLength'] and self.word_count(element) <= self.max_key_length) or not self.props['maxKeyLength']:
                c_product.append(element)

        return c_product

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