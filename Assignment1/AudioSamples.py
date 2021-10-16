import wave
import math
import numpy as np
import matplotlib.pyplot as plt


class Audiowave:

    def __init__(self, filedir):
        self.filedir = filedir
        self.wavedata = []
        self.wavewidth = 2
        self.wavechannel = 2
        self.framerate = 0
        self.Timedata = []
        self.nframes = 0

    # # 得到语音参数: 声道，采样宽度，帧速率，帧数，唯一标识，无损

    def waveopen(self):
        wf = wave.open(self.filedir, "rb")
        self.nframes = wf.getnframes() #音频帧数
        self.wavedata = wf.readframes(self.nframes) #读取并返回最多n帧音频，此处是返回全部音频，频率以bytes形式保存
        self.wavewidth = wf.getsampwidth() #采样位数
        self.wavechannel = wf.getnchannels() #声道数
        self.framerate = wf.getframerate() #采样频率
        time = self.nframes / self.framerate
        bps = self.framerate * self.wavewidth * 8 * self.wavechannel
        print("总帧数：" + str(self.nframes) + "帧")
        print("采样率：" + str(self.framerate) + "帧/s")
        print("声道数：" + str(self.wavechannel) + "个")
        print("位深：" + str(self.wavewidth * 8) + "bit")
        print("比特率：" + str(bps / 1000) + "kbps")
        print("时间：" + str(time) + "s")
        print("文件大小：" + str(time * bps / 8 / 1000) + "KB")
        return self.wavedata, self.wavewidth, self.wavechannel, self.framerate, time

    def wavehex_to_DEC(self, wavedata, wavewidth, wavechannel):
        n = int(len(wavedata) / wavewidth)
        i = 0
        j = 0
        for i in range(0, n):
            b = 0
            for j in range(0, wavewidth):
                temp = wavedata[i * wavewidth:(i + 1) * wavewidth][j] * int(math.pow(2, 8 * j))
                b += temp
            if b > int(math.pow(2, 8 * wavewidth - 1)):
                b = b - int(math.pow(2, 8 * wavewidth))
            self.Timedata.append(b)
        self.Timedata = np.array(self.Timedata)
        self.Timedata.shape = -1, wavechannel
        self.Timedata = self.Timedata.T
        x = np.linspace(0, len(self.Timedata[0]), len(self.Timedata[0])) / self.framerate
        # print(len(self.Timedata))
        # print(self.Timedata)
        return x, self.Timedata

    def to_fft(self, data):
        N = self.nframes  # 取样点数
        df = self.framerate / (N - 1)  # 分辨率
        freq = [df * n for n in range(0, N)]
        wave_data2 = data[0:N]
        c = np.fft.fft(wave_data2) * 2 / N
        d = int(len(c) / 2)
        freq = freq[:d - 1]
        fredata = abs(c[:d - 1])

        return freq, fredata

    def wavedraw(self):
        self.waveopen()
        timedata = self.wavehex_to_DEC(self.wavedata, self.wavewidth, self.wavechannel)


        print('########################')
        # waveData = waveData * 1.0 / max(abs(waveData))
        print(timedata)
        print(len(timedata[0]))
        print(len(timedata[1][0]))
        timedata_MinMax = timedata[1][0] * 1.0 / max(abs(timedata[1][0]))
        print(timedata_MinMax)
        print('########################')

        fredata_tuple = self.to_fft(timedata_MinMax)
        fredata = np.array(fredata_tuple,dtype=float)
        print('fredata',fredata)
        fredata = fredata / len(fredata)
        # fredata = np.log10(fredata)

        print('########################')

        plt.figure(figsize=(16, 8))
        plt.subplot(2, 1, 1)
        plt.plot(timedata[0], timedata_MinMax)
        plt.xlim(0, 4.5)

        plt.xlabel("Time(s)")
        plt.ylabel("Amplitude(V)")
        plt.title("Audio sample: Time domain")
        plt.subplot(2, 1, 2)
        # plt.plot(fredata[0], fredata[1])
        plt.plot(np.log10(fredata[0]), 20*np.log10(fredata[1]))
        plt.xlim(0, 4.5)
        plt.xlabel("Frequency(kHz)")
        plt.ylabel("Amplitude(dB)")
        plt.title("Frequency domain")

        plt.subplots_adjust(hspace=0.4)
        plt.show()


a=Audiowave(r"original.wav").wavedraw()

