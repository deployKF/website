document.addEventListener("DOMContentLoaded", function () {

    /* Set up search events */
    if (document.forms.search) {
        var query = document.forms.search.query
        query.addEventListener("blur", function () {
            if (this.value) zaraz.track("search", {search_term: this.value})
        })
    }

    /* Set up feedback events */
    document$.subscribe(function () {
        var feedback = document.forms.feedback
        if (typeof feedback === "undefined") return

        /* Send feedback */
        for (var button of feedback.querySelectorAll("[type=submit]")) {
            button.addEventListener("click", function (ev) {
                ev.preventDefault()

                /* Retrieve and send data */
                var page = document.location.pathname
                var data = this.getAttribute("data-md-value")
                zaraz.track("feedback", {page, data})

                /* Disable form and show note, if given */
                feedback.firstElementChild.disabled = true
                var note = feedback.querySelector(".md-feedback__note [data-md-value='" + data + "']")
                if (note) note.hidden = false
            })

            /* Show feedback */
            feedback.hidden = false
        }
    })
})