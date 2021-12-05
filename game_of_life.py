import numpy as np
import cv2


kernel = np.uint8([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
ALIVE = 1
DEAD = 0
THRESH = 0.8

H = 50
W = 150

def decide(current, neighbours):
    if current == ALIVE:
        # Any live cell with two or three live neighbours survives.
        if 2 <= neighbours <= 3:
            return ALIVE
        else:
            return DEAD
    elif current == DEAD:
        # Any dead cell with three live neighbours becomes a live cell.
        if neighbours == 3:
            return ALIVE

    # All other live cells die in the next generation. Similarly,
    # all other dead cells stay dead.
    return current
    


def next_gen(frame:np.ndarray) -> np.ndarray:
    next_frame = np.zeros_like(frame)
    
    for i in range(1, frame.shape[0] - 1):
        for j in range(1, frame.shape[1] - 1):
            neighbours = np.sum(kernel*frame[i-1:i+2, j-1:j+2])
            status = decide(frame[i, j], neighbours)
            next_frame[i, j] = status
            
    return next_frame


def generate_first_frame():
    seed = np.random.rand(H, W)
    frame = np.zeros((H+2, W+2), dtype=np.uint8)
    
    for i in range(seed.shape[0]):
        for j in range(seed.shape[1]):
            frame[i+1, j+1] = ALIVE if seed[i, j] > THRESH else DEAD
            
    return frame


def render_frame(frame):
    frame = frame[1:-1, 1:-1]
    rendered = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
    rendered[:, :, 1] = frame * 255 # Green channel
    
    rendered = cv2.resize(rendered, (W*8, H*8), interpolation=cv2.INTER_NEAREST)
    
    return rendered


if __name__ == '__main__':
    frame = generate_first_frame()
    key = 0

    while key not in (ord('q'), ord('Q')):
        rendered_frame = render_frame(frame)
        cv2.imshow('Game of Life', rendered_frame)
        key = cv2.waitKey(1)
        frame = next_gen(frame)