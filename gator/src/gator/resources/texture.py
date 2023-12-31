from OpenGL.GL import *
import PIL.Image as PillowImage
import ctypes

class Texture:
    def __init__(self, filePath: str):
        if not filePath: return
        self.assetName = "UnregisteredTexture"
        self.filePath: str = filePath
        
        pillowImage = PillowImage.open(
            f"{filePath}").transpose(PillowImage.FLIP_TOP_BOTTOM)
        imageData = pillowImage.tobytes()
        
        self.ID: int = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.ID)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        
        self.width, self.height = pillowImage.width, pillowImage.height
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, self.width,
                     self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, imageData)
        
        pillowImage.close()
        self.unbind()

    @classmethod
    def asFrameBuffer(cls, width: int, height: int):
        self = Texture(None)
        self.assetName: str = "[Generated]FramebufferTexture"
        self.filePath: str = "[Generated]"
        self.ID: int = glGenTextures(1)
        self.width, self.height = width, height
        glBindTexture(GL_TEXTURE_2D, self.ID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, ctypes.c_void_p(0))
        return self

    def destroy(self):
        glDeleteTextures(1, [self.ID])
        return self

    def bind(self, slot: int = 0):
        glActiveTexture(GL_TEXTURE0+slot)
        glBindTexture(GL_TEXTURE_2D, self.ID)
        return self

    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, GL_NONE)
        return self
