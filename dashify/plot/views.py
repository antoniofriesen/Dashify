from django.shortcuts import render

# Function to render the plots
def plot_data(request):
    return render(request, "plot/plot.html")
