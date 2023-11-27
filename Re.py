# 单词编码映射表
word_mapping = {
    'main'  : 1 ,'int'   : 2 ,'float' : 3,
    'if'    : 4 ,'else'  : 5 ,'while' : 6,
    '||'    : 7 ,'&&'    : 8 ,'!'     : 9,
    '='     : 13,'+'     : 14,'-'     : 15,'*'    : 16,'/'    : 17,
    '<'     : 18,'<='    : 19,'>'     : 20,'>='   : 21,
    '=='    : 22,'!='    : 23,
    ';'     : 24,','     : 25,
    '('     : 26,')'     : 27,'{'     : 28,'}'    : 29,
    '标识符': 10,
    '整型常数': 11,
    '实型常数': 12,
    }

# 拆分规则
def split_rules(source_code):
    tokens = []
    current_token = ''
    in_word = False

    for char in source_code:
        if char.isalnum() or char == '_':
            current_token += char
            in_word = True
        elif in_word:
            tokens.append(current_token)
            current_token = ''
            in_word = False

        if char in '(){}=!<>*+-/,;':
            if in_word:
                tokens.append(current_token)
                current_token = ''
                in_word = False
            tokens.append(char)

    if in_word:
        tokens.append(current_token)

    return tokens



# 处理整型常数
def process_integer(token, word_count, integer_constant, flags):
    if flags:
        if token not in integer_constant:
            integer_constant.append(token)
            word_count['整型常数'] = word_count.get('整型常数', 100) + 1
        else:
            word_count['整型常数'] = 1
        output = f"{word_mapping['整型常数']:<6} {word_count['整型常数']:<3} "
    else:
        if token not in integer_constant:
            integer_constant.append(token)
            word_count['整型常数'] = word_count.get('整型常数', 100) + 1
        else:
            return None
        output = f"{word_count['整型常数']:<6} {token:<3} "

    return output

# 处理实型常数
def process_real(token, word_count, real_constant, flags):
    if flags:
        if token not in real_constant:
            real_constant.append(token)
            word_count['实型常数'] = word_count.get('实型常数', -1) + 1
        else:
             word_count['实型常数'] = 1
        output = f"{word_mapping['实型常数']:<6} {word_count['实型常数']:<3} "
    else:
        if token not in real_constant:
            real_constant.append(token)
            word_count['实型常数'] = word_count.get('实型常数', -1) + 1
        else:
            return None
        output = f"{word_count['实型常数']:<6} {token:<3} "
    
    return output

# 处理标识符
def process_identifier(token, word_count, identifier, flags):
    if flags:
        if token not in identifier:
            identifier.append(token)
            word_count['标识符'] = word_count.get('标识符', 0) + 1
        else:
            word_count['标识符'] = 1
        output = f"{word_mapping['标识符']:<6} {word_count['标识符']:<3} "
    else:
        if token not in identifier:
            identifier.append(token)
            word_count['标识符'] = word_count.get('标识符', 0) + 1
        else:
            return None
        output = f"{word_count['标识符']:<6} {token:<3} "

    return output

# 处理整型常数，实型常数，标识符之外的单词
def process_others(token, word_count, others, flags):
    output = ""
    if flags:
        others.append(token)
        word_count[token] = word_count.get(token, 0)
        output = f"{word_mapping[token]:<6} {word_count[token]:<3} "
    else:
        return None


    return output



# 判断是否为整型常数
def is_integer(token):
    for char in token:
        if not char.isdigit():
            return False
    return True

# 判断是否为实型常数
def is_float(token):
    decimal_point_count = 0
    for char in token:
        if char.isdigit():
            continue
        elif char == '.':
            decimal_point_count += 1
            if decimal_point_count > 1:
                return False
        else:
            return False
    return decimal_point_count == 1



# 根据单词的内容决定调用相应的处理函数
def process_word(token, word_count, integer_constant, real_constant, identifier, others, flags):
    if flags:
        if token in word_mapping:
            output = process_others(token, word_count, others, flags)
        elif is_integer(token):
            output = process_integer(token, word_count, integer_constant, flags)
        elif is_float(token):
            output = process_real(token, word_count, real_constant, flags)
        else:
            output = process_identifier(token, word_count, identifier, flags)
    else:
        if token in word_mapping:
            output = process_others(token, word_count, others, flags)
        elif is_integer(token):
            output = process_integer(token, word_count, integer_constant,flags)
        elif is_float(token):
            output = process_real(token, word_count, real_constant,flags)
        else:
            output = process_identifier(token, word_count, identifier,flags)

    return output



# 完成任务 输出token.txt
def get_token(file_path):

    with open(file_path, 'r') as f:
        source_code = f.read()

    tokens = split_rules(source_code)


    word_count          = {}    #记录源代码中各种类型单词的出现次数
    integer_constant    = []    #存储源代码中出现的整型常数
    real_constant       = []    #存储源代码中出现的实型常数
    identifier          = []    #存储源代码中出现的标识符
    others              = []    #存储源代码中除整型常数、实型常数、标识符外的单词
    output_list         = []    #存储输出信息

    flags = True
    for token in tokens:
        output = process_word(token, word_count, integer_constant, real_constant, identifier, others, flags)
        if output:
            output_list.append(output)

    for output in output_list:
        print(output)

    # 将输出写入到 token.txt 文件中
    with open('token.txt', 'w') as output_file:
        for output in output_list:
            output_file.write(output + '\n')

# 完成任务 输出symbol.txt
def get_symbol(file_path):

    with open(file_path, 'r') as f:
        source_code = f.read()

    tokens = split_rules(source_code)


    word_count          = {}    #记录源代码中各种类型单词的出现次数
    integer_constant    = []    #存储源代码中出现的整型常数
    real_constant       = []    #存储源代码中出现的实型常数
    identifier          = []    #存储源代码中出现的标识符
    others              = []    #存储源代码中除整型常数、实型常数、标识符外的单词
    output_list         = []    #存储输出信息

    flags = False
    for token in tokens:
        output = process_word(token, word_count, integer_constant, real_constant, identifier, others, flags)
        if output:
            output_list.append(output)

    for output in output_list:
        print(output)

    # 将输出写入到 symbol.txt 文件中
    with open('symbol.txt', 'w') as output_file:
        for output in output_list:
            output_file.write(output + '\n')



get_token('source.txt')
get_symbol('source.txt')