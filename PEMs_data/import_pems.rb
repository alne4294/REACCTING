#!/usr/bin/ruby

require 'rubygems'
require 'csv'
# require "/Library/Ruby/Gems/2.0.0/gems/mongo-1.11.1/lib/mongo"
require 'mongo'
require 'json'
# include Mongo
# require "json/pure"
require "open-uri"

def create_indexes( collection )
  collection.create_index("predicted_CO")
  collection.create_index("predicted_NO")
  collection.create_index("predicted_CO2")
  collection.create_index("predicted_NO2")
  collection.create_index("predicted_VOC")
  collection.create_index("predicted_COZIR")
  collection.create_index("date")
  collection.create_index("iso_date")
  collection.create_index("day")
end

if ARGV.size != 2
 puts "Usage: ruby import_pems.rb <pems.csv> <pems_collection_name>"
 exit 0
end

#Parse the day that the measurements was taken from the filename
fileName = File.basename(ARGV[0])
dataType, remaining = fileName.split("_", 2)
testingDay, fileExt1, fileExt2 = remaining.split(".",3)
col_name   = ARGV[1]
print testingDay

if (testingDay.length != 8)
  raise ArgumentError, 'Is this a corrupt file name?... Should be dataType_dayNum.TXT.csv'
end

db   = Mongo::Connection.new.db('pems')
col  = db.collection(col_name)
create_indexes( col )

puts "The collection has #{col.count} document(s) at start."
puts "Reading from #{fileName}"

CSV.foreach('/Users/alexianewgord/Desktop/hmwk_5/PEMs_data/pemsWithDate/CSV/'+fileName, :headers => true) do |row|

   date = row[47]

   #Add a field with the searchable iso_date format
   year, month, remaining = date.split("-",3)
   day, remaining = remaining.split(" ",2)
   hour, min, sec = remaining.split(":",3)

   isoDateTime = Time.utc(year.to_i,month.to_i,day.to_i,hour.to_i,min.to_i,sec.to_i, "+00:00")

   doc = { \
  'Baseline' => row[1].to_f, \
  'CO2' => row[2].to_f, \
  'Fig1AkaCOZIR' => row[4].to_f, \
  'Fig2' => row[5].to_f, \
  'E2V_O3' => row[6].to_f, \
  'E2V_NO2' => row[7].to_f, \
  'E2V_1' => row[8].to_f, \
  'E2V_2_CO_' => row[9].to_f, \
  'E2V_3_VOC_' => row[10].to_f, \
  'E2V_4' => row[11].to_f, \
  'Temp' => row[12].to_f, \
  'Rh' => row[13].to_f, \
  'BMPtemp' => row[14].to_f, \
  'MBPPressure' => row[15].to_f, \
  'statSig1' => row[33].to_f, \
  'statSig2' => row[35].to_f, \
  'statSig3' => row[37].to_f, \
  'statSig4' => row[39].to_f, \
  'file_data' => row[40].to_f, \
	'predicted_NO2' => row[41].to_f, \
	'predicted_CO' => row[42].to_f, \
	'predicted_NO' => row[43].to_f, \
	'predicted_CO2' => row[44].to_f, \
	'predicted_COZIR' => row[45].to_f, \
  'predicted_VOC' => row[46].to_f, \
	'date' => date, \
	'iso_date' => isoDateTime, \
  'day' => testingDay.to_i \
	}

   col.save(doc)

end

puts "The collection now has #{col.count} document(s)."