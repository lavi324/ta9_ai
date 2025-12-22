# Windows installation:
For windows installation just follow [official instructions](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/how-to-use-codec-compressed-audio-input-streams?tabs=windows%2Cdebian%2Cjava-android%2Cterminal&pivots=programming-language-csharp#tabpanel_1_windows).
# Docker installation:
For Linux docker installation add these lines to **Dockerfile**:
`RUN apt-get update`
`RUN apt-get -y install libgstreamer1.0-0 gstreamer1.0-dev gstreamer1.0-tools gstreamer1.0-doc`
`RUN apt-get -y install gstreamer1.0-plugins-base gstreamer1.0-plugins-good `
`RUN apt-get -y install gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly `
## **Example:**
![image.png](/.attachments/image-559024d2-4eb7-44ef-826f-f6a265c33c44.png)