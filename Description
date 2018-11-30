# Computer Networks Team Project - Netowrk Application

## Description

Design an application layer protocol for three network entities:
* Controller (*C*)
* Renderer (*R*)
* Server (*S*)

The protocol should be text-based and well documented.
Teams should start designing and documenting the protocol before implementing a network application that uses this protocol.
A protocol specification *(refer to one of the **RFCs** on the **IETF's** web page for information on protocol documentation)* must be submitted at the end of the project.
The purpose of the protocol is to allow C to request a list of media files *(for example a text or video file)* from ***S***, then  ***C*** can request ***R*** to render the chosen file.
***R***, upon receiving a request from ***C***, sends a request to ***S*** so that ***S*** can stream the chosen media file to ***R*** for rendering.
***R*** has a limitation, it does not have the capability to buffer so it just renders what it receives from ***S***.
During the streaming session, ***C*** can request ***R*** to pause/resume/start-from-the-beginning the streaming.

Use *mininet* to implement a network application that allows a user to use ***C*** to request a list of media files stored on ***S***, and select one that the user is interested in.
***C*** then asks ***R*** to request a streaming session with ***S***, and ***S*** starts streaming the selected file to ***R*** for rendering *(note the limitation of ***R*** mentioned above).*
During a rendering session, the user can use ***C*** to control the rendering, e.g. pause/resume/start-from-the beginning. 

***C***, ***R*** and ***S*** must run on different hosts simulated using mininet and use the protocol designed by the team for communications.

For media file types, at the minimum text files must be supported.
