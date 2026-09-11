"""
War metadata module providing historical context, country information, flag icons,
and leader profiles for countries involved in war interactions.
"""

WAR_METADATA = {
    'Ethiopia': {
        'country': 'Ethiopia',
        'flag_url': 'https://flagcdn.com/w160/et.png',
        'leader': 'Abiy Ahmed',
        'leader_role': 'Prime Minister of Ethiopia (2018–present)',
        'leader_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Abiy_Ahmed_in_2020.jpg/330px-Abiy_Ahmed_in_2020.jpg',
        'era_context': 'Tigray War (2020–2022) and regional conflict interactions in Northern and Central Ethiopia.',
        'nostalgia_quote': 'Peace is not the absence of war, but the virtue born from strength of spirit and compromise.'
    },
    'Syria': {
        'country': 'Syria',
        'flag_url': 'https://flagcdn.com/w160/sy.png',
        'leader': 'Bashar al-Assad',
        'leader_role': 'President of Syria (2000–present)',
        'leader_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Bashar_al-Assad_%282018-05-17%29_02.jpg/330px-Bashar_al-Assad_%282018-05-17%29_02.jpg',
        'era_context': 'Syrian Civil War (2011–present), involving state armed forces, allied coalitions, and opposition groups.',
        'nostalgia_quote': 'War tests the ultimate endurance of nations and leaves echoes in history across generations.'
    },
    'Mexico': {
        'country': 'Mexico',
        'flag_url': 'https://flagcdn.com/w160/mx.png',
        'leader': 'Andrés Manuel López Obrador',
        'leader_role': 'President of Mexico (2018–2024)',
        'leader_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Andr%C3%A9s_Manuel_L%C3%B3pez_Obrador_in_2023.jpg/330px-Andr%C3%A9s_Manuel_L%C3%B3pez_Obrador_in_2023.jpg',
        'era_context': 'Mexican Drug War and non-state violent conflict interactions involving organized armed groups.',
        'nostalgia_quote': 'True security comes from justice and understanding the deeply rooted causes of conflict.'
    },
    'Afghanistan': {
        'country': 'Afghanistan',
        'flag_url': 'https://flagcdn.com/w160/af.png',
        'leader': 'Hibatullah Akhundzada / Ashraf Ghani',
        'leader_role': 'Key Figures during War Transition (2021–2022)',
        'leader_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Ashraf_Ghani_2019.jpg/330px-Ashraf_Ghani_2019.jpg',
        'era_context': 'War in Afghanistan (2001–2021) and subsequent power shifts and armed clashes.',
        'nostalgia_quote': 'The mountains of the Hindu Kush have witnessed centuries of warrior history and struggle.'
    },
    'Ukraine': {
        'country': 'Ukraine',
        'flag_url': 'https://flagcdn.com/w160/ua.png',
        'leader': 'Volodymyr Zelenskyy',
        'leader_role': 'President of Ukraine (2019–present)',
        'leader_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Volodymyr_Zelensky_Official_portrait.jpg/330px-Volodymyr_Zelensky_Official_portrait.jpg',
        'era_context': 'Russo-Ukrainian War and 2022 invasion, marking the largest European armed conflict since WWII.',
        'nostalgia_quote': 'Light will win over darkness, and history will record the heroic defense of our freedom.'
    },
    'Yemen': {
        'country': 'Yemen',
        'flag_url': 'https://flagcdn.com/w160/ye.png',
        'leader': 'Rashad al-Alimi / Mahdi al-Mashat',
        'leader_role': 'Yemeni Conflict Leadership (2014–present)',
        'leader_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Rashad_al-Alimi.jpg/330px-Rashad_al-Alimi.jpg',
        'era_context': 'Yemeni Civil War involving state forces, Houthi movement, and international coalition intervention.',
        'nostalgia_quote': 'Ancient Arabia Felix holds the memory of resilient communities surviving hardship.'
    },
    'Sudan': {
        'country': 'Sudan',
        'flag_url': 'https://flagcdn.com/w160/sd.png',
        'leader': 'Abdel Fattah al-Burhan vs. Mohamed Hamdan Dagalo',
        'leader_role': 'SAF Commander vs. RSF Commander',
        'leader_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Abdel_Fattah_al-Burhan_%282019-11-25%29.jpg/330px-Abdel_Fattah_al-Burhan_%282019-11-25%29.jpg',
        'era_context': 'Sudanese Armed Conflict (2023–present) between the Sudanese Armed Forces and Rapid Support Forces.',
        'nostalgia_quote': 'The waters of the Nile carry the tears and resilience of a nation fighting for stable peace.'
    },
    'Myanmar': {
        'country': 'Myanmar',
        'flag_url': 'https://flagcdn.com/w160/mm.png',
        'leader': 'Min Aung Hlaing',
        'leader_role': 'Chairman of State Administration Council',
        'leader_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Min_Aung_Hlaing_%282021-04-24%29.jpg/330px-Min_Aung_Hlaing_%282021-04-24%29.jpg',
        'era_context': 'Myanmar Civil War following the 2021 coup, engaging ethnic armed organizations and PDF forces.',
        'nostalgia_quote': 'Across golden pagodas and dense forests, generations have longed for tranquil harmony.'
    }
}

DEFAULT_METADATA = {
    'country': 'Global Conflict Zone',
    'flag_url': 'https://flagcdn.com/w160/un.png',
    'leader': 'Regional Military Command',
    'leader_role': 'Conflict Actors & Defense Forces',
    'leader_image': 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=300&q=80',
    'era_context': 'Documented Georeferenced Organized Violence and Armed Interactions.',
    'nostalgia_quote': 'War is where the young and brave give their all; history remembers their stories.'
}

def get_country_metadata(country_name):
    """
    Returns metadata dict for a given country, or default if not specifically listed.
    """
    return WAR_METADATA.get(country_name, {
        'country': country_name,
        'flag_url': 'https://flagcdn.com/w160/un.png',
        'leader': f'Leader of {country_name}',
        'leader_role': 'Head of State / Military Command',
        'leader_image': 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=300&q=80',
        'era_context': f'Active conflict interactions recorded in {country_name}.',
        'nostalgia_quote': 'History records the brave, the fallen, and the hope for eventual peace.'
    })
