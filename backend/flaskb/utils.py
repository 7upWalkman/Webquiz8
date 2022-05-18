"""
Common Python utilities used throughout the project.

(c) Joao Galamba, 2022
$LICENSE(MIT)
"""

################################################################################
##
##      STRINGs
##
################################################################################

def camel_to_snake_case(ident: str) -> str:
    """
    abcXpto  -> abc_xpto
    abc      -> abc
    abcXYpto -> abc_x_ypto
    """
    return ''.join((f'_{ch.lower()}' if ch.isupper() else ch) for ch in ident)
#:

def snake_to_camel_case(ident: str) -> str:
    """
    abc_xpto    -> abcXpto
    abc         -> abc
    abc_x_ypto  -> abcXYpto
    abc____xpto -> abcXpto
    abc_        -> abc
    abc__       -> abc
    """
    tokens = ident.split('_')
    return tokens[0] + ''.join(
        (token[0].upper() + token[1:] if token else '') for token in tokens[1:]
    )
#:
