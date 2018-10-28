from discovery_api.models import Activity, Category, KeyWord, Location

class SearchBar():
    def search_str(filter):
        activities=[]
        keywords=[]
        categories=[]
        for s in filter.split():
            stripped_s=s.strip().lower()
            #print(stripped_s)
            activities+=Activity.objects.filter(name__icontains=stripped_s)
            categories+=Category.objects.filter(name__icontains=stripped_s)
            keywords+= KeyWord.objects.filter(tag__icontains=stripped_s)
        print(keywords)
        for c in categories:
            activities += Activity.objects.filter(category=c)
            keywords += KeyWord.objects.filter(category=c)

        loc=[]
        loc+=Location.objects.filter(activities__in=activities)
        loc+=Location.objects.filter(keyWords__in=keywords)
        #Location.objects.filter(keyWords__in=keywords)
        return(set(loc))

