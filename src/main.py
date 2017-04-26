from pipeline.pipeline import Pipeline

if __name__ == '__main__':
    from sys import argv
    try:
        filename = argv[1]
    except:
        print("Usage: pipeline filename")
        from sys import exit
        exit()
    params = {'source':filename}
    pipeline = Pipeline(params)
    pipeline.buildVisualization()
