SELECT nom,prenom from client 
inner join reservation on client.id_client = reservation.id_client
inner join chambre on reservation.id_chambre = chambre.id_chambre
where sum(id_chambre)>1
group by client.id_client

select sum (total) from paiement where month(date)=2

select count(id_chambre) from reservation inner join chambre