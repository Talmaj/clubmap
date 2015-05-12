 #!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import string
import re
pd.set_option('max_colwidth', 400)

def split_and_expand(series, on):
    """
    Splits and expands the rows on a certain separator
    """
    tmp = series.str.lower().str.split(on)
    tmp = tmp.apply(pd.Series)
    c = tmp.unstack(level=-1)
    c = c.dropna()
    c = c.reset_index(drop=True)
    c = c.drop_duplicates()
    return c

def single_filter_check(df, mask):

    if len(df[mask]) == 1:
        return df

    for i in df[mask].index:
        print '\nKeep the following entry? y/n'
        print df.ix[i, 'raw']
        
        inp = raw_input()
        # making sure input is correct
        while inp not in ['y', 'n']:
            print '\nKeep the following entry? y/n'
            print '\n'.join(df.ix[i, 'raw'])
            inp = raw_input()

        if inp == 'n':
            df = df.drop(i)
        elif inp == 'y':
            continue
    return df

def filter_check(df, mask):
    if not len(df[mask]): return df
    print '\nKeep all the following entries? y/n'
    print '\n'.join(df.ix[mask, 'raw'])
    inp = raw_input()

    if inp == 'n':
        return df[~mask]
    elif inp == 'y':
        return single_filter_check(df, mask)
    else:
        return filter_check(df, mask)

def select_info(df, sep='/|\||:| - '):   
    tmp = df['raw'].str.split(sep)#
    mask = tmp.apply(len) > 1
    drp_indx = []
    for i in tmp[mask].index:
        print '\nSelect one of the elements or write the name'
        print df.ix[i, 'raw']
        print tmp.ix[i], 
        inp = raw_input()
        
        if inp.isdigit():
            inp = int(inp) - 1
            try:
                df.ix[i, 'raw'] = tmp.ix[i][inp].strip()
            except IndexError:
                print 'Index Error:'
                inp = raw_input()
                inp = int(inp) - 1
                df.ix[i, 'raw'] = tmp.ix[i][inp].strip()
        elif inp in ['del', 'delete', 'd']:
            drp_indx.append(i)
        else:
            df.ix[i, 'raw'] = inp

    df = df.drop(drp_indx)
    return df
            
        
def clean_lineup(line_up):
    if type(line_up) != list:
        line_up = line_up.strip('\r\n').strip()
        line_up = line_up.split('\r\n')
    df = pd.DataFrame(line_up, columns=['raw'])
    df = df.dropna()

    # Extract label before split_and_expand, could be also bad (we loose label info), try different approaches
    df['label'] = df['raw'].str.findall(u'\(.*?\)|\[.*?\]|〔.*?〕')
    df['rm'] = df['label'].apply(lambda x: '|'.join(re.escape(w) for w in x))
    df['raw'] = df.apply(lambda row: re.sub(row['rm'], '', row['raw']), axis=1)

    # removes all the sentences that end on either .!? and contain at least one of the words in ident
    ident = ['dance', 'floor', 'bar', 'our', 'you', 'will', 'music']
    mask = df['raw'].str.lower().str.contains('\s' + '\s|\s'.join(ident) + '\s') & df['raw'].str.contains('.{25}[\?\.!]<br />$')
    df = filter_check(df, mask)

    # splits the rows where the artist are written in one line and separated by the one of the separators
    separators = [',', '//', ' & ', ' b2b ', ' \+ ']
    tmp = split_and_expand(df['raw'], '|'.join(separators))
    df = pd.DataFrame(tmp, columns=['raw'])

    # getting dj name from url and alias from aka
    df['href'] = df['raw'].str.findall('href="(.*?)"')
    df['raw'] = df['raw'].str.replace(' AKA | a\.k\.a ', ' aka ')
    tmp = df['raw'].str.split(' aka ')
    df['aka'] = tmp.str.get(1)
    df['raw'] = tmp.str.get(0)

    # remove html tags
    df['raw'] = df['raw'].str.replace('<.+?>', '')
    df['aka'] = df['aka'].str.replace('<.+?>', '').str.strip()
    # strip punctuation

    # playing mit dj_name
    mask = df['raw'].str.contains('\smit\s')
    df.ix[mask, 'raw'] = df.ix[mask, 'raw'].str.split('\smit\s').str.get(1)

    # striping punctuation
    df['raw'] = df['raw'].str.strip().str.strip(string.punctuation).str.strip()

    df['raw'] = df['raw'].str.replace('^tresor[:\s]', '', flags=re.IGNORECASE).str.strip()

    # removing some not good dj names
    rm = ['berlin', 'residents', '', 'panorama bar', 'panoramabar', 'berghain', 'live', 'visuals', 'acid bogen', 'open air',
          'tba', 'more tba', 'garten', 'microkorg',
          'raw residents', 'tresor', 'acidbogen', 'indoor', 'featured artists', 'tbc', 'neue heimat', 'secret lineup',
          'music', 'art', 'techno', 'dj', 'djs', 'jazzy nerlin jam session', 'leipzig', 'newcomerfloor', 'hall', 'silo', 'sexy',
          'g', '&', 'many more']
    mask = df['raw'].str.lower().isin(rm)
    df = df[~mask]

    # removing some obvious regexes
    regexes = ['(^|[-\s])floor($|\s)', '(^|[-\s])stage($|\s)', '^tresor[:\s]', 'special guest', '(^|\s)tba($|\s)',
               '^berghain[:\s]', '^panorama ?bar[:\s]', 'open decks', '^doors[:\s]', '^show[:\s]', 'mainfloor', 'after hour',
               '\sparty\s', '\sroom\s', '^garten[:\s]']
    mask = df['raw'].str.lower().str.contains('|'.join(regexes))#.str.contains('(^|[-\s])stage($|\s)')
    df = filter_check(df, mask)

    # remove the places from the back of the strings
    places = ['berlin', 'iran', 'australia', 'usa', 'amsterdam', 'paris', 'italy', 'portugal', 'japan', 'israel']
    df['raw'] = df['raw'].str.replace('\s' + '$|\s'.join(places) + '$', '', flags=re.IGNORECASE)

    # striping punctuation
    df['raw'] = df['raw'].str.strip().str.strip(string.punctuation).str.strip()

    # remove weird unicode signs (stars, etc.)
    signs = [u'\u2606',u'\u2605', u'\u25cf', u'\xb0', u'\u2022', u'\u25a0', u'\u318d', u'\u25a0',
                u'\u02c6', u'\u0ad0']
    df['raw'] = df['raw'].str.strip(''.join(signs)).str.strip()
    mask = df['raw'].str.contains(u'|'.join(signs))
    df = filter_check(df, mask)

    # remove the live tags
    df['raw'] = df['raw'].str.replace('\s\*?live|^live[:\s]', '', flags=re.IGNORECASE)

    df['raw'] = df['raw'].str.strip().str.strip(string.punctuation).str.strip()

    df = select_info(df)
    df['raw'] = df['raw'].str.strip()
    # delete here the delete entries
    line_up = df.raw.str.lower().unique().tolist() + df.aka.str.lower().unique().tolist()

    return line_up








