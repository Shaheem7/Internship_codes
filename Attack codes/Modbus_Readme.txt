
First make sure local goose library is present
If not, then use below commands 

cd <folder_name>
cd ..

## For help 

python <script_name> -h

## For live capture ##
    
    python3 <script_name> --livecapture --store <filename>

## For offline execution ##
    python3 <script_name> --pcapfile <filename>

make sure temporary pcap filename.pcapng should be present, if not then use 

touch temp.pcapng