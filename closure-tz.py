import datetime
from pprint import pprint
import json

from pytz import timezone, all_timezones
from icu import TimeZone, Locale

epoch = datetime.datetime(1970,1,1)


def build_names(zone):
	names = []
	tzicu = TimeZone.createTimeZone(zone)
	names.append(tzicu.getDisplayName(False, 1))
	names.append(tzicu.getDisplayName(False, 2))

	if tzicu.useDaylightTime():
		names.append(tzicu.getDisplayName(True, 1))
		names.append(tzicu.getDisplayName(True, 2))
	return names

def build_std_offset(zone):
	tzicu = TimeZone.createTimeZone(zone)
	return tzicu.getRawOffset() / 1000 / 60

def build_transitions(tz):
	trans = []
	if not hasattr(tz, '_utc_transition_times'):
		return trans

	for idx, d1 in enumerate(tz._utc_transition_times):
		if (d1.year < 1970):
			continue

		dst_offset = int(tz._transition_info[idx][1].total_seconds() / 60)
		utc_offset = int((d1 - epoch).total_seconds() / 3600)
		trans.append(utc_offset)
		trans.append(dst_offset)
	return trans


def build_zone(zone):
	tz = timezone(zone)
	std_offset = build_std_offset(zone)
	trans = build_transitions(tz)
	names = build_names(zone)

	return {
		'id': tz.zone,
		'transitions': trans,
		'std_offset': std_offset,
		'names': names
	}


def main():
	import os
	import shutil
	shutil.rmtree('data')

	for zone in all_timezones:
		path = 'data/' + zone + '.json'
		dir_path = os.path.dirname(path)
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)

		with open(path, 'w+') as f:
			json.dump(build_zone(zone), f, sort_keys=True, indent=2)

if __name__ == "__main__":
	main()
