form Save time and pitch in one file for all Pitch objects
    folder Output_folder /Users/josefhavlas/Downloads/praat_pitches/monolog/MSA
endform

createFolder: output_folder$

n = numberOfSelected("Pitch")
if n = 0
    exitScript: "Please select one or more Pitch objects first."
endif

for i from 1 to n
    pitchIDs [i] = selected("Pitch", i)
endfor

for i from 1 to n
    selectObject: pitchIDs [i]
    pitchName$ = selected$()

    numberOfFrames = Get number of frames
    outFile$ = output_folder$ + "/" + pitchName$ + ".txt"

    # first line: overwrite/create file
    t = Get time from frame number: 1
    v = Get value in frame: 1, "Hertz"

    if v = undefined
        writeFileLine: outFile$, string$ (t), tab$, "nan"
    else
        writeFileLine: outFile$, string$ (t), tab$, string$ (v)
    endif

    # remaining lines: append
    for frame from 2 to numberOfFrames
        t = Get time from frame number: frame
        v = Get value in frame: frame, "Hertz"

        if v = undefined
            appendFileLine: outFile$, string$ (t), tab$, "nan"
        else
            appendFileLine: outFile$, string$ (t), tab$, string$ (v)
        endif
    endfor

    appendInfoLine: "Saved: ", outFile$
endfor

writeInfoLine: "Done. ", string$ (n), " saved pitches to: ", output_folder$