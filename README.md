# Distributed-Project
This project implements a 2D multiplayer Car Racing Game usingpygame. Players can control their cars and compete against each other. The game features real-time communication, score tracking, and enemy cars for added challenge.

This game utilizes various technologies and concepts, like Sockets Programming to establish communication between the game server and connected clients. Sockets allow for real-time data transmission over the network. Also Threading is employed to handle multiple client connections concurrently. Each client is assigned a separate thread, allowing for simultaneous gameplay and communication.</br>


we have two python files:

<ol>
  <li> The <b> server.py </b> file contains the server-side implementation of the game. It uses sockets to establish connections with multiple clients and coordinate the gameplay.</li> 
<li>The <b>client.py</b> file contains the client-side implementation of the game. It connects to the server and allows players to control their cars.</li>
  </ol>

# Requirements
Before running the game, ensure that you have the following software installed on your system:
<ul>
  <li>Python 3.x</li>
  <li>pygame library</li>
  <li>pymongo library</li>
 </ul> 

# How to Run and Play the Game
<ol>
  <li>Run the <b>server.py</b> script on a server machine.</li>
  <li>Run the <b>client.py</b> script on each client machine.</li>
  <li> A window will apear to enter a name for the player then press enter.</li>
  <li> Once connected, you will see your car on the track. Use the arrow keys to control the car:
   <ul>
     <li>Up Arrow: Move the car up (accelerate) </li>
     <li>Down Arrow: Move the car down</li>
     <li> Left Arrow: Move the car to the left</li>
     <li>Right Arrow: Move the car to the right</li>
    </ul></li>
  <li>Avoid collision with enemy cars and try to score as many points as possible.If client crashed, he/she will be removed from the game and from other players’ screens</li>
  <li> Use the chatbox at the bottom of the screen to communicate with other players. Type your message and press Enter to send it.</li>

  <li>Players' scores are displayed on the screen.The game will continue until one of the players reaches a score of 3000 points, at which point the game will end for all players. </li>
  </br>
  </ol>
  
 # Snippets of players playing the game
 
 <p> Two players playing and one of them started using the chatting feature</p>

![Picture2](https://github.com/hamzaayman216/Distributed-Project/assets/90004229/03be8970-7314-45e6-8f3b-4bfbb9774ffe)


</br>
</br>
<p> One of the players crashed while the other is still playing .</p>

![Picture1](https://github.com/hamzaayman216/Distributed-Project/assets/90004229/117f06d2-c8c0-4848-9551-ca54a72c58b8)

 </br>

# Video link
https://drive.google.com/file/d/1CC0sFKgS3wTzXy2WBe6uZ1OWKAFQotJ1/view?usp=sharing
