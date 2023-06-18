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
  </br>
  
  ![image](https://github.com/hamzaayman216/Distributed-Project/assets/90004229/4c339b60-b389-45bc-9891-f97e2faa9aa2)

  
  <li>Run the <b>client.py</b> script on each client machine.</li>
  </br>
  
  ![image](https://github.com/hamzaayman216/Distributed-Project/assets/90004229/d6b4d7e0-98c4-4416-9eb2-9a22eb5106a1)

  
  <li> A window will apear to enter a name for the player.</li>
  </br>
  
 ![image](https://github.com/hamzaayman216/Distributed-Project/assets/90004229/23787073-dff7-4d45-922f-b4e5da102eae)
  
  
  <li> The player will click Enter and wait for other players to connect to the server. </li>
  </br>
  
  ![image](https://github.com/hamzaayman216/Distributed-Project/assets/90004229/89948eb7-00df-49c9-8cf8-1d3a368dbabf)

  
  <li> Once connected, you will see your car on the track. Use the arrow keys to control the car:
   <ul>
     <li>Up Arrow: Move the car up (accelerate) </li>
     <li>Down Arrow: Move the car down</li>
     <li> Left Arrow: Move the car to the left</li>
     <li>Right Arrow: Move the car to the right</li>
    </ul></li>
  </br>
  
  ![image](https://github.com/hamzaayman216/Distributed-Project/assets/90004229/52304e7f-4b6c-463b-928a-60050841c8ec)

  
<li> Use the chatbox at the bottom of the screen to communicate with other players. Type your message and press Enter to send it.</li>
  </br>
  
  ![image](https://github.com/hamzaayman216/Distributed-Project/assets/90004229/df7226d8-844e-47dd-9f05-1145fc62a2c0)

  
  ![image](https://github.com/hamzaayman216/Distributed-Project/assets/90004229/6a985b51-f186-4e82-9896-5771fd69d6bb)
</br>
  
  <li>Avoid collision with enemy cars and try to score as many points as possible.If player crashed, he/she will be removed from the game and from other players’ screens</li>
  </br>
  
  ![image](https://github.com/hamzaayman216/Distributed-Project/assets/90004229/f9f125b1-049e-4ae8-befb-f644d960ade5)

  <li>Players' scores are displayed on the screen.The game will continue until one of the players reaches a score of 3000 points, at which point the game will end for all players. </li> 
  </br>
  
![image](https://github.com/hamzaayman216/Distributed-Project/assets/90004229/32e52eeb-decf-4dac-81a3-e8b6b4eaef2a)

  
  </br>
  </ol>
  
<!--  # Snippets of players playing the game
 
 <p> Two players playing and one of them started using the chatting feature</p>

![Picture2](https://github.com/hamzaayman216/Distributed-Project/assets/90004229/03be8970-7314-45e6-8f3b-4bfbb9774ffe)


</br>
</br>
<p> One of the players crashed while the other is still playing .</p>

![Picture1](https://github.com/hamzaayman216/Distributed-Project/assets/90004229/117f06d2-c8c0-4848-9551-ca54a72c58b8)

 </br>
 -->
# Video link
https://drive.google.com/file/d/1CC0sFKgS3wTzXy2WBe6uZ1OWKAFQotJ1/view?usp=sharing
