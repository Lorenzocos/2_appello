class ExameException(Exception):
    pass

class CSVTimeSeriesFile:
    def __init__(self, name):
        self.name = name
    def get_data(self):
        lista_di_coppie = []
        FileCSV = open(self.name, 'r')
        #per avere un confronto che mi garantisca la crescenza
        epoch_prec = -1
        for line in FileCSV:
            info = line.split(',')
            #trascuro così la prima riga contenente "epoch,temperature"
            if info[0] != 'epoch':
                #controllo che i valori restanti siano numeri senza alzare eccezioni
                try:
                    float(info[0])
                    float(info[1])
                except:
                    continue
                #controllo che la serie sia strettamente crescente alzando in caso un'eccezione
                if round(int(info[0])) > epoch_prec:
                    epoch_prec = round(float(info[0]))
                    lista_di_coppie.append(info)
                else:
                    raise ExameException("Attenzione, la serie 'epoch' non è ordinata")
                    epoch_prec = round(float(info[0]))
                    lista_di_coppie.append(info)
        FileCSV.close()
        return lista_di_coppie

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()

def hourly_trend_changes(time_series):
    numero_inversioni_trend = []

    first = True
    var = 0 #numero di variazioni
    delta = 0 #variazione con la prima temperatura precedente diversa
    for info in time_series:
        #il blocco funzionza solo per il primo ciclo
        if first:
            epoch = round(float(info[0]))
            temp = float(info[1])
            ora = epoch //3600
            first = False
        #dal secondo ciclo in poi
        else:
            epoch = round(float(info[0]))
            #controllo se ho un cambiamento di crescenza/decrescenza
            if delta*(float(info[1])-temp) < 0:
                var+=1
            #il delta lo si calcola se ho temperature diverse, altrimenti rimane l'ultimo valore assegnato
            if info[1] != temp:
                delta = float(info[1])-temp
            temp = float(info[1])
            #controllo se sono nella stessa ora
            if ora == epoch // 3600:
                ora = epoch //3600
                continue
            #altrimenti aggiungo var alla lista
            else:
                numero_inversioni_trend.append(var)
                ora = epoch //3600
                var = 0
    return numero_inversioni_trend
