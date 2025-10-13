"""
===============================================================================
EAPrompt Context Definitions
===============================================================================

This file contains example prompts and instruction templates used for implementing **EAPrompt** — a framework for translation error analysis and evaluation.

The contents include:
    1. Example prompt contexts for different language pairs (En-De, En-Ru, Zh-En)
       - `*_REF` examples include both source and reference translations.
       - `*_SRC` examples include only the source and the translation.
       - `*_ERROR_DETAILED` and `*_ERROR_ITEMIZED` provide demonstration of how detailed and itemized error annotations should look.
       - `*_COUNT` provides example outputs for error counting.

    2. Instruction templates guiding the model behavior during evaluation.
       - `INSTRUCTION_ERROR_REF` and `INSTRUCTION_ERROR_SRC` instruct models to identify major and minor translation errors.
       - `INSTRUCTION_COUNT` instructs models to output only the error counts.
       - `INSTRUCTION_SINGLESTEP_*` combines both steps into a single task.

    3. Evaluation input formats.
       - `EVALUATION_INPUT_REF` is used when a reference translation is available.
       - `EVALUATION_INPUT_SRC` is used when no reference is available.

These definitions are intended for prompt construction and controlled evaluation of translation quality under the EAPrompt framework. 
Each constant serves as a reusable component in downstream evaluation or training pipelines.
===============================================================================
"""

#### Examples ####

## En-De ##

EXAMPLE_ENDE_REF = """
Source: They were addressed to her son, who has autism and lives in a private care facility, she said. But instead of her son's name inside when you opened them, the letters said Dear Maine's Department of Health and Human Services -- in Cincinnati, she told local media.
Reference: Sie seien an ihren Sohn adressiert, der an Autismus leidet und in einer privaten Pflegeeinrichtung lebt, sagte sie. Aber als Sie die Briefe öffnete, stand darin nicht der Name ihres Sohnes, sondern sie waren an das Gesundheitsministerium von Maine gerichtet, in Cincinnati, wie sie den lokalen Medien sagte.
Translation: Sie wurden an ihren Sohn gerichtet, der Autismus hat und in einer privaten Pflegeeinrichtung lebt, sagte sie. Aber anstelle des Namens ihres Sohnes im Inneren, als Sie sie öffneten, sagten die Briefe Dear Maine 's Department of Health and Human Services -- in Cincinnati, sagte sie den lokalen Medien.
"""

EXAMPLE_ENDE_SRC = """
Source: They were addressed to her son, who has autism and lives in a private care facility, she said. But instead of her son's name inside when you opened them, the letters said Dear Maine's Department of Health and Human Services -- in Cincinnati, she told local media.
Translation: Sie wurden an ihren Sohn gerichtet, der Autismus hat und in einer privaten Pflegeeinrichtung lebt, sagte sie. Aber anstelle des Namens ihres Sohnes im Inneren, als Sie sie öffneten, sagten die Briefe Dear Maine 's Department of Health and Human Services -- in Cincinnati, sagte sie den lokalen Medien.
"""

EXAMPLE_ERROR_DETAILED_ENDE = """
I think the mistranslation of "Sie" should be categorized into a major error, and the untranslated text in "Dear Maine 's Department of Health and Human Services" should also considered as a major error. "sagten" and "im Inneren" are both mistranslation errors, they should be categorized into minor errors. The omission of "Briefe ,," should be considered as a minor error. "wurden" is a grammar error, which should also be considered as a minor error. "im Inneren, als Sie sie öffneten, sagten die Briefe" is awkward in style, and should be also considered as a minor error.
"""

EXAMPLE_ERROR_ITEMIZED_ENDE = """
Major errors:
(1) “Sie” – Mistranslation
(2) “Dear Maine 's Department of Health and Human Services” – Untranslated text
Minor errors:
(1) “sagten” – Mistranslation
(2) “im Inneren” – Mistranslation
(3) “Briefe ,,” – Omission
(4) “wurden” – Grammar
(5) “im Inneren, als Sie sie öffneten, sagten die Briefe” – Awkward Style
"""

EXAMPLE_COUNT_ENDE = "2, 5"

## En-Ru ##

EXAMPLE_ENRU_REF = """
Source: Experience fast-paced, action-packed combat, hunt monsters and huge bosses, fight with friends in a guild to siege nodes and castles, and train in a variety of life skills such as fishing, trading, crafting, cooking, sailing, and much more!
Reference: Опробуйте быстроразвивающийся насыщенный событиями бой, охоту на монстров и огромных боссов, сражайтесь с друзьями в гильдии, чтобы осаждать центры и замки, а также тренируйте множество жизненных навыков, таких как рыболовство, торговля, создание предметов, готовка, мореходство и многие другие!
Translation: Испытайте быстро развивающийся, насыщенный бой, охотитесь на монстров и огромных боссов, сражайтесь с друзьями в гильдии, чтобы осадить узлы и замки, и тренируйтесь в различных жизненных навыках, таких как рыбалка, торговля, крафтинг, приготовление пищи, парусный спорт и многое другое!
"""

EXAMPLE_ENRU_SRC = """
Source: Experience fast-paced, action-packed combat, hunt monsters and huge bosses, fight with friends in a guild to siege nodes and castles, and train in a variety of life skills such as fishing, trading, crafting, cooking, sailing, and much more!
Translation: Испытайте быстро развивающийся, насыщенный бой, охотитесь на монстров и огромных боссов, сражайтесь с друзьями в гильдии, чтобы осадить узлы и замки, и тренируйтесь в различных жизненных навыках, таких как рыбалка, торговля, крафтинг, приготовление пищи, парусный спорт и многое другое!
"""

EXAMPLE_ERROR_DETAILED_ENRU = """
I think the inconsistency of "Испытайте" and "охотитесь" should both be categorized into major errors. "таких как" and "многое другое" should be both also considered as two minor errors on agreement. "узлы" and "парусный спорт" are both mistranslation errors, they should be categorized into minor errors.
"""

EXAMPLE_ERROR_ITEMIZED_ENRU = """
Major errors:
(1) "Испытайте" – Inconsistency
(2) "охотитесь" – Inconsistency
Minor errors:
(1) "таких как" – Agreement
(2) "многое другое” – Agreement
(3) "узлы" – Mistranslation
(4) "парусный спорт" – Mistranslation
"""

EXAMPLE_COUNT_ENRU = "2, 4"

## Zh-En ##

EXAMPLE_ZHEN_REF = """
Source: 中新网北京9月27日电 (记者 杜燕)为加强节前市场监管执法，北京市市场监管局在国庆节前夕检查各类经营主体2000余户。
Reference: Chinanews.com Report on September 27 in Beijing (Journalist Du Yan) The Beijing Administration for Market Regulation inspected more than 2,000 operating entities of different types before the National Day holiday to strengthen pre-holiday market regulation and law enforcement.
Translation: BEIJING, Sept. 27 (Reporter Du Yan) In order to strengthen market supervision and law enforcement before the festival, the Beijing Municipal Market Supervision Bureau inspected more than 2,000 households of various business subjects on the eve of the National Day.
"""

EXAMPLE_ZHEN_SRC = """
Source: 中新网北京9月27日电 (记者 杜燕)为加强节前市场监管执法，北京市市场监管局在国庆节前夕检查各类经营主体2000余户。
Translation: BEIJING, Sept. 27 (Reporter Du Yan) In order to strengthen market supervision and law enforcement before the festival, the Beijing Municipal Market Supervision Bureau inspected more than 2,000 households of various business subjects on the eve of the National Day.
"""

EXAMPLE_ERROR_DETAILED_ZHEN = """
I think the mistranslation of "subjects" should be categorized into a major error, and the omission in "BEIJING" should also considered as a major error. "households of various", "festival" and "supervision" are three mistranslation errors, they should be categorized into minor errors. The terminology, "Beijing Municipal Market Supervision Bureau" is inappropriate for context, and should also be categorized into a minor error, which is considered as a minor error.
"""

EXAMPLE_ERROR_ITEMIZED_ZHEN = """
Major errors:
(1) “BEIJING” – Omission
(2) “subjects” – Mistranslation
Minor errors:
(1) “households of various” – Mistranslation
(2) “festival” – Mistranslation
(3) “supervision” – Mistranslation
(4) “Beijing Municipal Market Supervision Bureau” – Inappropriate for context
(5) “BEIJING” – Spelling'
"""

EXAMPLE_COUNT_ZHEN = "2, 5"

#### Instructions ####

INSTRUCTION_ERROR_REF = """
Based on the given source and reference, identify the major and minor errors in this translation. Note that Major errors refer to actual translation or grammatical errors, and Minor errors refer to smaller imperfections, and purely subjective opinions about the translation.
"""

INSTRUCTION_ERROR_SRC = """
Based on the given source, identify the major and minor errors in this translation. Note that Major errors refer to actual translation or grammatical errors, and Minor errors refer to smaller imperfections, and purely subjective opinions about the translation.
"""

INSTRUCTION_COUNT = """
Based on the above error information, Output 2 numbers ONLY with the format: "x, x", indicating the number of major and minor errors. DO NOT ADD other information!
"""

INSTRUCTION_SINGLESTEP_REF = """
Based on the given source and reference, identify the major and minor errors in this translation. Note that Major errors refer to actual translation or grammatical errors, and Minor errors refer to smaller imperfections, and purely subjective opinions about the translation.
Then based on the error information, Output 2 numbers ONLY with the format: "x, x", indicating the number of major and minor errors. DO NOT ADD other information!
"""

INSTRUCTION_SINGLESTEP_SRC = """
Based on the given source, identify the major and minor errors in this translation. Note that Major errors refer to actual translation or grammatical errors, and Minor errors refer to smaller imperfections, and purely subjective opinions about the translation.
Then based on the error information, Output 2 numbers ONLY with the format: "x, x", indicating the number of major and minor errors. DO NOT ADD other information!
"""

#### Evaluation Input ####

EVALUATION_INPUT_REF = """
Source: {src}
Reference: {ref}
Translation: {tgt}
"""

EVALUATION_INPUT_SRC = """
Source: {src}
Translation: {tgt}
"""
