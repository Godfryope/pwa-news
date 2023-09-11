const subscribeUser = async () => {
    try {
        const registration = await navigator.serviceWorker.register('{% static "js/service-worker.js" %}');
        const subscription = await registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: 'BHZqP-XBPHNfO1UrQ24u8RKuYN-vuX0whEjGM8qeHJXkKltcEEbzPPQaV11KNv3mlDmgt3irhidcw96b9Ble83s'
        });
        // Send the subscription data to the server
        await fetch('/subscribe/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': 'Your_CSRF_Token'  // Add your CSRF token here
            },
            body: `subscription=${JSON.stringify(subscription)}`
        });
        console.log('Subscribed successfully');
    } catch (error) {
        console.error('Subscription failed:', error);
    }
};
