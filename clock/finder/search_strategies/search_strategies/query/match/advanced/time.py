from clock.finder.search_strategies.search_strategies.query.match.advanced import AdvancedMatchSearchStrategy
from clock.finder.zone_finder.zone_finders.localized_date_time import LocalizedDateTimeZoneFinder


class TimeMatchSearchStrategy(AdvancedMatchSearchStrategy):
    def __init__(self, query_lower: str, localized_date_time_zone_finder: LocalizedDateTimeZoneFinder):
        super().__init__(query_lower, localized_date_time_zone_finder)

    def search(self):
        self.time_search()

    def time_search(self):
        results = self.localized_date_time_zone_finder.match_time_lower(self.query_lower)
        self._add_results(results)
