from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

line_of_cars = {"change_oil": [], "inflate_tires": [], "diagnostic": []}
ticket_no = 0
time_required = 0
processed = []


class MainPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, "tickets/cautionpage.html")


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        template = "Welcome to the Hypercar Service!"
        return HttpResponse(template)


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "tickets/menu.html")


class TaskView(View):
    def get(self, request, task, *args, **kwargs):
        global ticket_no
        global time_required
        global processed
        if task == "change_oil":
            time_required = len(line_of_cars["change_oil"]) * 2
            ticket_no += 1
            line_of_cars["change_oil"].append(ticket_no)
        elif task == "inflate_tires":
            time_required = len(line_of_cars["change_oil"]) * 2 + len(line_of_cars["inflate_tires"]) * 5
            ticket_no += 1
            line_of_cars["inflate_tires"].append(ticket_no)
        elif task == "diagnostic":
            time_required = len(line_of_cars["change_oil"]) * 2 + len(line_of_cars["inflate_tires"]) * 5 + len(line_of_cars["diagnostic"]) * 30
            ticket_no += 1
            line_of_cars["diagnostic"].append(ticket_no)
        context = {"ticket_id": ticket_no, "time": time_required}
        return render(request, "tickets/infopage.html", context=context)


class ProcessingView(View):
    def get(self, request, *args, **kwargs):
        context = {"oil_len": len(line_of_cars["change_oil"]),
                   "inflate_len": len(line_of_cars["inflate_tires"]),
                   "diagnostic_len": len(line_of_cars["diagnostic"])
                   }
        return render(request, "tickets/processingpage.html", context=context)

    def post(self, request, *args, **kwargs):
        global processed
        if line_of_cars["change_oil"]:
            processed.append(line_of_cars["change_oil"][0])
            line_of_cars["change_oil"] = line_of_cars["change_oil"][1:]
        elif line_of_cars["inflate_tires"]:
            processed.append(line_of_cars["inflate_tires"][0])
            line_of_cars["inflate_tires"] = line_of_cars["inflate_tires"][1:]
        elif line_of_cars["diagnostic"]:
            processed.append(line_of_cars["diagnostic"][0])
            line_of_cars["diagnostic"] = line_of_cars["diagnostic"][1:]
        return redirect("/next")


class NextPage(View):
    def get(self, request, *args, **kwargs):
        empty = False
        number_of_ticket = 0
        if processed:
            number_of_ticket = processed[-1]
        else:
            empty = True
        context = {"empty": empty, "next_ticket": number_of_ticket}
        return render(request, "tickets/ticketpage.html", context=context)
