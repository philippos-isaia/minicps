// Generated by binpac_quickstart

#ifndef ANALYZER_PROTOCOL_ENIP_ENIP_H
#define ANALYZER_PROTOCOL_ENIP_ENIP_H

#include "events.bif.h"


#include "analyzer/protocol/tcp/TCP.h"

#include "enip_pac.h"

namespace analyzer { namespace enip {

class ENIP_Analyzer

: public tcp::TCP_ApplicationAnalyzer {

public:
	ENIP_Analyzer(Connection* conn);
	virtual ~ENIP_Analyzer();

	// Overriden from Analyzer.
	virtual void Done();
	virtual void DeliverStream(int len, const u_char* data, bool orig);
	virtual void Undelivered(uint64 seq, int len, bool orig);

	// Overriden from tcp::TCP_ApplicationAnalyzer.
	virtual void EndpointEOF(bool is_orig);

	static analyzer::Analyzer* InstantiateAnalyzer(Connection* conn)
		{ return new ENIP_Analyzer(conn); }

protected:
	binpac::ENIP::ENIP_Conn* interp;
	bool had_gap;
};

} } // namespace analyzer::*

#endif