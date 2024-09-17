
First make sure local goose library is present
If not, then use below commands 

cd <folder_name>
cd ..

## For help 

python <script_name> -h

## For running the script online ##

python <script_name> --livecapture --output <filename>


## For offline execution ##

python <script_name> --pcapfile <filename>

make sure temporary pcap filename.pcapng should be present, if not then use 

touch temp.pcapng