document.addEventListener("DOMContentLoaded", function () {

    window.dataLayer = window.dataLayer || []

    function gtag() {
        dataLayer.push(arguments)
    }

    /* Set up search events */
    if (document.forms.search) {
        var query = document.forms.search.query
        query.addEventListener("blur", function () {
            if (this.value) gtag("event", "search", {search_term: this.value})
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
                gtag("event", "feedback", {page, data})

                /* Disable form and show note, if given */
                feedback.firstElementChild.disabled = true
                var note = feedback.querySelector(".md-feedback__note [data-md-value='" + data + "']")
                if (note) note.hidden = false
            })

            /* Show feedback */
            feedback.hidden = false
        }
    })

    /* Set up virtual page navigation events */
    var last_pathname = document.location.pathname
    location$.subscribe(function (url) {

        /* Do nothing if the URL path has not changed */
        if (last_pathname == url.pathname) return
        last_pathname = url.pathname

        /* Do nothing if zaraz is not available */
        if (typeof zaraz == "undefined") return
        if (typeof zarazData == "undefined") return

        /* Send virtual page navigation event */
        zarazData.l = document.location.href
        zarazData.t = document.title
        zaraz.pageVariables = {}
        zaraz.track("__zarazSPA")
    })
})