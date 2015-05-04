%% Convert any .mat files to csv, and save them near the location they came from

clear; close all;

%% GUI for data selection
if ispc == 1;slash = '\';else slash = '/';end
filenames = [];
Pathnames = {};
CancelOut = 0;
[filenames, Pathnames] = uigetfile((' *.mat; *.MAT'),'Select .mat files to convert to CSV','MultiSelect','on');
pathnames_csv = strcat(Pathnames,'CSV'); %New location to save csv files to.

if isequal(filenames,0); disp('No files selected, run ended'); break; end
allFiles = dir(pathnames_csv); allNames = { allFiles.name };
allPathName=strcat(pathnames_csv, allNames);

%% Loop through files, convert to .csv
for i = 1:length(filenames)
    if ischar(filenames)
        nameload = [Pathnames filenames];
    else
        nameload = [Pathnames filenames{i}];
    end
    try
        b=load(nameload);
        %The following line was added specifically for PEMS
        c = b.PEMScalibrated
        %Added for converting date format-----------------
        S = datestr(c.Unixtime, 31);
        tab = table(S, 'VariableNames',{'Date'});
        dateData = table2dataset(tab);
        a = horzcat(c,dateData);
        %End addition-------------------------------------
        fields = fieldnames(a)
        %If the file is not yet saved as csv, do so
        %Save to .csv file
        if ischar(filenames)
            nameloadcsv = [pathnames_csv slash filenames];
        else
            nameloadcsv = [pathnames_csv slash filenames{i}];
        end
        nameloadcsv = strrep(nameloadcsv,'.mat','.csv');
        if ~any(strcmp(nameloadcsv,allPathName))
            try
                export(a,'File',nameloadcsv,'Delimiter',',');
            catch err
                if ~exist(pathnames_csv, 'dir')
                    mkdir([pathnames_csv])
                end
                writetable(a.(fields{1}),nameloadcsv,'Delimiter',',','QuoteStrings',true)
            end
            
        end
    catch err
        disp(['Unable to convert file ' filenames{i} ]);
    end
end



