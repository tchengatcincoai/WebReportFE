DB_TIMESTAMP_ITEM_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "definitions": {},
    "id": "http://example.com/example.json",
    "properties": {
        "daily_user": {
            "default": 77777,
            "description": "An explanation about the purpose of this instance.",
            "id": "/properties/daily_user",
            "title": "The daily_user schema",
            "type": "integer"
        },
        "geo_contribution": {
            "id": "/properties/geo_contribution",
            "items": {
                "id": "/properties/geo_contribution/items",
                "properties": {
                    "country": {
                        "default": "US",
                        "description": "An explanation about the purpose of this instance.",
                        "id": "/properties/geo_contribution/items/properties/country",
                        "title": "The country schema",
                        "type": "string"
                    },
                    "pageviews": {
                        "default": 1,
                        "description": "An explanation about the purpose of this instance.",
                        "id": "/properties/geo_contribution/items/properties/pageviews",
                        "title": "The pageviews schema",
                        "type": "integer"
                    },
                    "rank": {
                        "default": "9511",
                        "description": "An explanation about the purpose of this instance.",
                        "id": "/properties/geo_contribution/items/properties/rank",
                        "title": "The rank schema",
                        "type": "string"
                    },
                    "users": {
                        "default": 0.69999999999999996,
                        "description": "An explanation about the purpose of this instance.",
                        "id": "/properties/geo_contribution/items/properties/users",
                        "title": "The users schema",
                        "type": "number"
                    }
                },
                "type": "object"
            },
            "type": "array"
        },
        "global_rank": {
            "default": 9999,
            "description": "An explanation about the purpose of this instance.",
            "id": "/properties/global_rank",
            "title": "The global_rank schema",
            "type": "integer"
        },
        "load_time": {
            "default": 33,
            "description": "An explanation about the purpose of this instance.",
            "id": "/properties/load_time",
            "title": "The load_time schema",
            "type": "integer"
        },
        "page_views_per_visitor": {
            "default": 4,
            "description": "An explanation about the purpose of this instance.",
            "id": "/properties/page_views_per_visitor",
            "title": "The page_views_per_visitor schema",
            "type": "integer"
        },
        "related_sites": {
            "id": "/properties/related_sites",
            "items": {
                "default": "cctv1.com",
                "description": "An explanation about the purpose of this instance.",
                "id": "/properties/related_sites/items",
                "title": "The 0 schema",
                "type": "string"
            },
            "type": "array"
        },
        "site_information": {
            "id": "/properties/site_information",
            "properties": {
                "company_name": {
                    "default": "yyy",
                    "description": "An explanation about the purpose of this instance.",
                    "id": "/properties/site_information/properties/company_name",
                    "title": "The company_name schema",
                    "type": "string"
                },
                "contact": {
                    "default": "xxx",
                    "description": "An explanation about the purpose of this instance.",
                    "id": "/properties/site_information/properties/contact",
                    "title": "The contact schema",
                    "type": "string"
                }
            },
            "type": "object"
        },
        "timestamp": {
            "default": 1,
            "description": "An explanation about the purpose of this instance.",
            "id": "/properties/timestamp",
            "title": "The timestamp schema",
            "type": "integer"
        },
        "top_key_words": {
            "id": "/properties/top_key_words",
            "items": {
                "id": "/properties/top_key_words/items",
                "properties": {
                    "keyword": {
                        "default": "a",
                        "description": "An explanation about the purpose of this instance.",
                        "id": "/properties/top_key_words/items/properties/keyword",
                        "title": "The keyword schema",
                        "type": "string"
                    },
                    "percent_of_search_traffic": {
                        "default": 11.199999999999999,
                        "description": "An explanation about the purpose of this instance.",
                        "id": "/properties/top_key_words/items/properties/percent_of_search_traffic",
                        "title": "The percent_of_search_traffic schema",
                        "type": "number"
                    }
                },
                "type": "object"
            },
            "type": "array"
        },
        "top_sites_linking_in": {
            "id": "/properties/top_sites_linking_in",
            "items": {
                "id": "/properties/top_sites_linking_in/items",
                "properties": {
                    "page": {
                        "default": "blog.sina.com.cn/s/blog_48ee6b9e0100",
                        "description": "An explanation about the purpose of this instance.",
                        "id": "/properties/top_sites_linking_in/items/properties/page",
                        "title": "The page schema",
                        "type": "string"
                    },
                    "site": {
                        "default": "sina.com.cn",
                        "description": "An explanation about the purpose of this instance.",
                        "id": "/properties/top_sites_linking_in/items/properties/site",
                        "title": "The site schema",
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "type": "array"
        },
        "upstream_sites": {
            "id": "/properties/upstream_sites",
            "items": {
                "id": "/properties/upstream_sites/items",
                "properties": {
                    "percent_of_unique_visits": {
                        "default": 1.8,
                        "description": "An explanation about the purpose of this instance.",
                        "id": "/properties/upstream_sites/items/properties/percent_of_unique_visits",
                        "title": "The percent_of_unique_visits schema",
                        "type": "number"
                    },
                    "site": {
                        "default": "xxx.com",
                        "description": "An explanation about the purpose of this instance.",
                        "id": "/properties/upstream_sites/items/properties/site",
                        "title": "The site schema",
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "type": "array"
        },
        "where_do_visitors_go_on": {
            "id": "/properties/where_do_visitors_go_on",
            "items": {
                "id": "/properties/where_do_visitors_go_on/items",
                "properties": {
                    "percent_of_visitors": {
                        "default": 1,
                        "description": "An explanation about the purpose of this instance.",
                        "id": "/properties/where_do_visitors_go_on/items/properties/percent_of_visitors",
                        "title": "The percent_of_visitors schema",
                        "type": "integer"
                    },
                    "subdomain": {
                        "default": "news.qq.com",
                        "description": "An explanation about the purpose of this instance.",
                        "id": "/properties/where_do_visitors_go_on/items/properties/subdomain",
                        "title": "The subdomain schema",
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "type": "array"
        }
    },
    "type": "object"
}
SAMPLE_DB_DATA = [
    {
        'web_address': 'cctv.com',
        'web_data': [
            {
                'timestamp': 1,
                'global_rank': 9999,
                'load_time': 33,
                'page_views_per_visitor': 4,
                'daily_user': 77777,
                'geo_contribution': [
                    # change to be numbers except for rank which could be null
                    {
                        "country": "US",
                        "pageviews": 1.0,
                        "users": 0.7,
                        "rank": "9511"
                    },
                    {
                        "country": "CN",
                        "pageviews": 0.7,
                        "users": 0.8,
                        "rank": "31269"
                    },
                    {
                        "country": "CA",
                        "pageviews": 6.5,
                        "users": 5.7,
                        "rank": "20833"
                    },
                    {
                        "country": "JP",
                        "pageviews": 89.3,
                        "users": 90.4,
                        "rank": "3365"
                    }
                ],
                'top_key_words': [
                    {"keyword": "a", "percent_of_search_traffic": 11.2},
                    {"keyword": "b", "percent_of_search_traffic": 5.2},
                    {"keyword": "c", "percent_of_search_traffic": 1.2}
                ],
                'related_sites': ['cctv1.com', 'cctv2.com'],
                'upstream_sites': [
                    {'site': 'xxx.com', 'percent_of_unique_visits': 1.8},
                    {'site': 'yyy.com', 'percent_of_unique_visits': 1.2}
                ],
                'where_do_visitors_go_on': [
                    {'subdomain': 'news.qq.com', 'percent_of_visitors': 1.0},
                    {'subdomain': 'v.qq.com', 'percent_of_visitors': 2.0}
                ],
                'site_information': {
                    'contact': 'xxx',
                    'company_name': 'yyy'
                },
                'top_sites_linking_in': [
                    {'site': 'sina.com.cn', 'page': 'blog.sina.com.cn/s/blog_48ee6b9e0100'},
                    {'site': 'csdn.net', 'page': 'blog.csdn.net/wish_silence/article/'},
                    {'site': 'naver.com', 'page': 'blog.naver.com/PostView.nhn?blogId=ch'}
                ]
            },
            {
                'timestamp': 2,
                'global_rank': 9949,
                'load_time': 35,
                'page_views_per_visitor': 3,
                'daily_user': 77737,
                'geo_contribution': [
                    {
                        "country": "US",
                        "pageviews": 1.0,
                        "users": 0.7,
                        "rank": "9511"
                    },
                    {
                        "country": "CN",
                        "pageviews": 0.7,
                        "users": 0.8,
                        "rank": "31269"
                    },
                    {
                        "country": "CA",
                        "pageviews": 6.5,
                        "users": 5.7,
                        "rank": "20833"
                    },
                    {
                        "country": "JP",
                        "pageviews": 89.3,
                        "users": 90.4,
                        "rank": "3365"
                    }
                ],
                'top_key_words': [
                    {"keyword": "a", "percent_of_search_traffic": 11.2},
                    {"keyword": "b", "percent_of_search_traffic": 5.2},
                    {"keyword": "c", "percent_of_search_traffic": 1.2}
                ],
                'related_sites': ['cctv1.com', 'cctv2.com'],
                'upstream_sites': [
                    {'site': 'xxx.com', 'percent_of_unique_visits': 1.8},
                    {'site': 'yyy.com', 'percent_of_unique_visits': 1.2}
                ],
                'where_do_visitors_go_on': [
                    {'subdomain': 'news.qq.com', 'percent_of_visitors': 1.0},
                    {'subdomain': 'v.qq.com', 'percent_of_visitors': 2.0}
                ],
                'site_information': {
                    'contact': 'xxx',
                    'company_name': 'yyy'
                },
                'top_sites_linking_in': [
                    {'site': 'sina.com.cn', 'page': 'blog.sina.com.cn/s/blog_48ee6b9e0100'},
                    {'site': 'csdn.net', 'page': 'blog.csdn.net/wish_silence/article/'},
                    {'site': 'naver.com', 'page': 'blog.naver.com/PostView.nhn?blogId=ch'}
                ]
            },
            {
                'timestamp': 3,
                'global_rank': 9549,
                'load_time': 45,
                'page_views_per_visitor': 2,
                'daily_user': 78737,
                'geo_contribution': [
                    {
                        "country": "US",
                        "pageviews": 1.0,
                        "users": 0.7,
                        "rank": "9511"
                    },
                    {
                        "country": "CN",
                        "pageviews": 0.7,
                        "users": 0.8,
                        "rank": "31269"
                    },
                    {
                        "country": "CA",
                        "pageviews": 6.5,
                        "users": 5.7,
                        "rank": "20833"
                    },
                    {
                        "country": "JP",
                        "pageviews": 89.3,
                        "users": 90.4,
                        "rank": "3365"
                    }
                ],
                'top_key_words': [
                    {"keyword": "a", "percent_of_search_traffic": 11.2},
                    {"keyword": "b", "percent_of_search_traffic": 5.2},
                    {"keyword": "c", "percent_of_search_traffic": 1.2}
                ],
                'related_sites': ['cctv1.com', 'cctv2.com'],
                'upstream_sites': [
                    {'site': 'xxx.com', 'percent_of_unique_visits': 1.8},
                    {'site': 'yyy.com', 'percent_of_unique_visits': 1.2}
                ],
                'where_do_visitors_go_on': [
                    {'subdomain': 'news.qq.com', 'percent_of_visitors': 1.0},
                    {'subdomain': 'v.qq.com', 'percent_of_visitors': 2.0}
                ],
                'site_information': {
                    'contact': 'xxx',
                    'company_name': 'yyy'
                },
                'top_sites_linking_in': [
                    {'site': 'sina.com.cn', 'page': 'blog.sina.com.cn/s/blog_48ee6b9e0100'},
                    {'site': 'csdn.net', 'page': 'blog.csdn.net/wish_silence/article/'},
                    {'site': 'naver.com', 'page': 'blog.naver.com/PostView.nhn?blogId=ch'}
                ]
            }
        ]
    },
    {
        'web_address': 'qq.com',
        'web_data': [
            {
                'timestamp': 1,
                'global_rank': 9999,
                'load_time': 33,
                'page_views_per_visitor': 4,
                'daily_user': 77777,
                'geo_contribution': [
                    {
                        "country": "US",
                        "pageviews": 1.0,
                        "users": 0.7,
                        "rank": "9511"
                    },
                    {
                        "country": "CN",
                        "pageviews": 0.7,
                        "users": 0.8,
                        "rank": "31269"
                    },
                    {
                        "country": "CA",
                        "pageviews": 6.5,
                        "users": 5.7,
                        "rank": "20833"
                    },
                    {
                        "country": "JP",
                        "pageviews": 89.3,
                        "users": 90.4,
                        "rank": "3365"
                    }
                ],
                'top_key_words': [
                    {"keyword": "a", "percent_of_search_traffic": 11.2},
                    {"keyword": "b", "percent_of_search_traffic": 5.2},
                    {"keyword": "c", "percent_of_search_traffic": 1.2}
                ],
                'related_sites': ['cctv1.com', 'cctv2.com'],
                'upstream_sites': [
                    {'site': 'xxx.com', 'percent_of_unique_visits': 1.8},
                    {'site': 'yyy.com', 'percent_of_unique_visits': 1.2}
                ],
                'where_do_visitors_go_on': [
                    {'subdomain': 'news.qq.com', 'percent_of_visitors': 1.0},
                    {'subdomain': 'v.qq.com', 'percent_of_visitors': 2.0}
                ],
                'site_information': {
                    'contact': 'xxx',
                    'company_name': 'yyy'
                },
                'top_sites_linking_in': [
                    {'site': 'sina.com.cn', 'page': 'blog.sina.com.cn/s/blog_48ee6b9e0100'},
                    {'site': 'csdn.net', 'page': 'blog.csdn.net/wish_silence/article/'},
                    {'site': 'naver.com', 'page': 'blog.naver.com/PostView.nhn?blogId=ch'}
                ]
            }
        ]
    }
]
