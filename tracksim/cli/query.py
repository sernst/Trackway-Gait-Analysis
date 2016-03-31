
def confirm(question, default = True):

    result = input('{question} [{yes}/{no}]:'.format(
        question=question,
        yes='(Y)' if default else 'Y',
        no='N' if default else '(N)'
    ))

    if not result:
        return default

    if result[0].lower() in ['y', 't', '1']:
        return True
    return False

