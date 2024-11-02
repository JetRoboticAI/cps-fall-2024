%Run initialization before starting this program
function data=process(x)
    recorder=audiorecorder(44100,16,1)
    recordblocking(recorder,3);
    audioData = getaudiodata(recorder); 
    f=pitch(audioData,44100,Range=[20,3999],Method="PEF") %calculates frequency
    data=trimmean(f,20)
end
    
function transmit=mqWrite(client,x)
    write(client,"TunerSynth769/Readings",string(x));
    transmit=1
end
StartCounter=0
while StartCounter>=0
    msg1=read(mqClient);
    try 
        msg=read(mqClient).Data(1)
    catch
        msg = 0;
    end
    if class(msg)=='string'
        data=process(1)
        transmit=mqWrite(mqClient,data)
        StartCounter=StartCounter+1
    end
end