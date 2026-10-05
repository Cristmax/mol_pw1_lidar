# ROS 2 virtuális akadályérzékelő

Egyszerű ROS 2 alapú virtuális akadályérzékelő rendszer az **Autonóm járművek és robotok programozása** tantárgy kis beadandó feladatához.

A projekt fizikai szenzor nélkül szimulál egy LIDAR szenzort, majd a generált mérési adatok alapján meghatározza a robot előtt található legközelebbi akadály távolságát.

## Működés

A rendszer két ROS 2 node-ból áll:

- `virtual_lidar` – virtuális LIDAR adatokat generál és `sensor_msgs/LaserScan` üzeneteket publikál a `/scan` topicra.
- `obstacle_detector` – feliratkozik a `/scan` topicra, feldolgozza a robot előtti méréseket, majd meghatározza a legközelebbi akadály távolságát.

A detektor három állapotot különböztet meg:

 Távolság  Állapot 

 0–1 m -> `AKADÁLY` 
 1–2 m -> `FIGYELEM` 
 2 m felett -> `SZABAD` 

## Felépítés


virtual_lidar
      |
      | sensor_msgs/LaserScan
      v
    /scan
      |
      v
obstacle_detector
      |
      v
SZABAD / FIGYELEM / AKADÁLY


## Követelmények

- Ubuntu
- ROS 2
- Python 3
- `colcon`

## Fordítás

A csomagot egy ROS 2 workspace `src` könyvtárába kell helyezni, majd:

```bash
cd ~/ajr_ws
colcon build
source install/setup.bash
```

## Használat

### Virtuális LIDAR indítása

Például 0,5 méterre elhelyezett virtuális akadállyal:

```bash
ros2 run virtual_obstacle_detector virtual_lidar --ros-args -p obstacle_distance:=0.5
```

### Akadályérzékelő indítása

Egy másik terminálban:

```bash
source ~/ajr_ws/install/setup.bash
ros2 run virtual_obstacle_detector obstacle_detector
```

Példa kimenet:

```text
AKADÁLY - Legközelebbi akadály: 0.50 m
```

A virtuális akadály távolsága az `obstacle_distance` paraméterrel adható meg.

Példák:

```bash
# AKADÁLY
ros2 run virtual_obstacle_detector virtual_lidar --ros-args -p obstacle_distance:=0.5

# FIGYELEM
ros2 run virtual_obstacle_detector virtual_lidar --ros-args -p obstacle_distance:=1.5

# SZABAD
ros2 run virtual_obstacle_detector virtual_lidar --ros-args -p obstacle_distance:=5.0
```

